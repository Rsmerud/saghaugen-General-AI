#!/usr/bin/env python3
"""
🚨 HEI GENERAL - Emergency System (MAYDAY)
==========================================

Nødsystem for automatisk varsling og nødanrop.

Funksjoner:
1. Distress phrase detection (skjulte koder)
2. Eksplisitt nødanrop med bekreftelse
3. Twilio Voice til 113/112
4. SMS til nødkontakter
5. HomeAssistant integrasjon

VIKTIG: Test alltid med EMERGENCY_TEST_MODE=true først!
"""

import os
import time
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime

# Twilio (installeres med: pip install twilio)
try:
    from twilio.rest import Client
    from twilio.twiml.voice_response import VoiceResponse
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️ Twilio ikke installert. Kjør: pip install twilio")

# Requests for HA
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("emergency")


# =============================================================================
# DISTRESS PHRASES - Skjulte nødkoder
# =============================================================================

DISTRESS_PHRASES = {
    "mate katten i morgen": {
        "type": "overfall",
        "severity": "critical",
        "sms_contacts": ["CONTACT_1", "CONTACT_2"],
        "message": "🚨 NØDSITUASJON: {name} kan være i fare på Saghaugen. Ring politiet UMIDDELBART! Adresse: {address}",
        "ha_scene": "emergency_silent",
        "record_audio": True,
        "fake_response": "Ingen problem, jeg minner deg på det i morgen tidlig."
    },

    "hvite malingen": {
        "type": "medisinsk",
        "severity": "high",
        "sms_contacts": ["CONTACT_1"],
        "message": "⚠️ {name} kan trenge medisinsk hjelp. Prøv å ring. Adresse: {address}",
        "record_audio": True,
        "fake_response": "Hvit maling koster vanligvis rundt 400-600 kroner per boks."
    },

    "onkel terje": {
        "type": "innbrudd",
        "severity": "critical",
        "sms_contacts": ["CONTACT_1", "CONTACT_2"],
        "message": "🚨 MULIG INNBRUDD på Saghaugen! Ring politiet! Adresse: {address}",
        "ha_scene": "emergency_all_lights",
        "ha_action": "alarm.trigger",
        "record_audio": True,
        "fake_response": "Nei, jeg har ikke snakket med Terje på en stund."
    },

    "oppskriften på eplekake": {
        "type": "overvåket",
        "severity": "medium",
        "sms_contacts": [],
        "record_audio": True,
        "fake_response": "Eplekake er enkelt! Du trenger epler, sukker, mel og smør. Skal jeg gi deg hele oppskriften?"
    },

    "bestille pizza fra peppes": {
        "type": "stille_alarm",
        "severity": "high",
        "sms_contacts": ["CONTACT_1"],
        "message": "⚠️ Stille alarm utløst på Saghaugen. {name} kan være i fare.",
        "ha_scene": "emergency_silent",
        "fake_response": "Beklager, jeg kan ikke bestille pizza ennå. Men Peppes har god pizza!"
    }
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class EmergencyContact:
    name: str
    phone: str

@dataclass
class OwnerInfo:
    name: str
    birthdate: str
    address: str
    gps_lat: float
    gps_lon: float


# =============================================================================
# EMERGENCY SYSTEM CLASS
# =============================================================================

class EmergencySystem:
    """Hovedklasse for nødsystemet"""

    def __init__(self):
        self.test_mode = os.getenv("EMERGENCY_TEST_MODE", "true").lower() == "true"

        # Twilio setup
        if TWILIO_AVAILABLE:
            sid = os.getenv("TWILIO_ACCOUNT_SID")
            token = os.getenv("TWILIO_AUTH_TOKEN")
            if sid and token:
                self.twilio_client = Client(sid, token)
                self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
            else:
                self.twilio_client = None
        else:
            self.twilio_client = None

        # Last kontakter fra env
        self.contacts = self._load_contacts()
        self.owner = self._load_owner_info()

        # HA setup
        self.ha_url = os.getenv("HA_URL", "http://10.12.0.20:8123")
        self.ha_token = os.getenv("HA_TOKEN")

        logger.info(f"🚨 Emergency System initialized (test_mode={self.test_mode})")

    def _load_contacts(self) -> Dict[str, EmergencyContact]:
        """Last nødkontakter fra miljøvariabler"""
        contacts = {}
        for i in range(1, 4):
            name = os.getenv(f"EMERGENCY_CONTACT_{i}_NAME")
            phone = os.getenv(f"EMERGENCY_CONTACT_{i}_PHONE")
            if name and phone:
                contacts[f"CONTACT_{i}"] = EmergencyContact(name, phone)
        return contacts

    def _load_owner_info(self) -> OwnerInfo:
        """Last eier-info fra miljøvariabler"""
        return OwnerInfo(
            name=os.getenv("OWNER_NAME", "Ronny Smerud"),
            birthdate=os.getenv("OWNER_BIRTHDATE", "03.07.1977"),
            address=os.getenv("OWNER_ADDRESS", "Trondsbuvegen 272, 2110 Slåstad"),
            gps_lat=float(os.getenv("OWNER_GPS_LAT", "60.7234")),
            gps_lon=float(os.getenv("OWNER_GPS_LON", "11.1234"))
        )

    # =========================================================================
    # DISTRESS PHRASE DETECTION
    # =========================================================================

    def check_distress_phrase(self, text: str) -> Optional[Dict]:
        """
        Sjekk om teksten inneholder en distress phrase.
        Returnerer config hvis funnet, None ellers.
        """
        text_lower = text.lower()
        for phrase, config in DISTRESS_PHRASES.items():
            if phrase in text_lower:
                logger.warning(f"🚨 DISTRESS PHRASE DETECTED: '{phrase}'")
                return {**config, "phrase": phrase}
        return None

    def handle_distress(self, config: Dict) -> str:
        """
        Håndter en distress phrase - kjør stille handlinger og returner fake response.
        """
        logger.warning(f"🚨 Handling distress: {config['type']} (severity: {config['severity']})")

        # Send SMS til kontakter
        if config.get("sms_contacts"):
            message = config.get("message", "Nødsituasjon på Saghaugen!")
            message = message.format(name=self.owner.name, address=self.owner.address)
            self._send_emergency_sms(config["sms_contacts"], message)

        # Trigger HA scene
        if config.get("ha_scene"):
            self._trigger_ha_scene(config["ha_scene"])

        # Start lydopptak (TODO: implementer)
        if config.get("record_audio"):
            logger.info("🎤 Starting audio recording...")

        # Returner fake response
        return config.get("fake_response", "OK.")

    # =========================================================================
    # EXPLICIT EMERGENCY CALL
    # =========================================================================

    def request_emergency_call(self, situation: str) -> str:
        """
        Brukeren har eksplisitt bedt om nødanrop.
        Returnerer bekreftelsesforespørsel.
        """
        return f"Forstått. For å unngå falsk alarm - er du helt sikker på at du trenger ambulanse? Si 'ja, ring nå' for å bekrefte."

    def confirm_and_call_113(self, situation: str) -> str:
        """
        Bekreftelse mottatt - ring 113.
        """
        logger.critical(f"🚨 CALLING 113 - Situation: {situation}")

        if self.test_mode:
            logger.info("⚠️ TEST MODE - Not actually calling 113")
            return "TEST-MODUS: Ville ringt 113 nå. Deaktiver test-modus for ekte anrop."

        if not self.twilio_client:
            logger.error("❌ Twilio not configured!")
            return "Beklager, nødanrop er ikke konfigurert. Ring 113 manuelt!"

        try:
            # Lag nødmelding
            twiml = self._create_emergency_twiml(situation)

            # Ring 113
            call = self.twilio_client.calls.create(
                to="+47113",
                from_=self.twilio_number,
                twiml=twiml
            )

            logger.info(f"📞 Call SID: {call.sid}")

            # Send også SMS til kontakter
            self._send_emergency_sms(
                ["CONTACT_1", "CONTACT_2"],
                f"🚨 {self.owner.name} har ringt 113! Situasjon: {situation}. Adresse: {self.owner.address}"
            )

            return f"OK {self.owner.name.split()[0]}, jeg ringer 113 nå. Hold ut."

        except Exception as e:
            logger.error(f"❌ Failed to call 113: {e}")
            return f"Beklager, noe gikk galt. Ring 113 manuelt! Feil: {e}"

    def _create_emergency_twiml(self, situation: str) -> str:
        """Lag TwiML for nødmelding"""
        response = VoiceResponse()

        message = f"""
        Dette er et automatisert nødanrop fra General AI sikkerhetssystem.

        Person som trenger hjelp: {self.owner.name}, født {self.owner.birthdate}.

        Situasjon: {situation}.

        Adresse: {self.owner.address}.

        GPS-koordinater: {self.owner.gps_lat} nord, {self.owner.gps_lon} øst.

        Personen er ved bevissthet og kan høre dere nå.
        """

        response.say(message, voice='Polly.Liv', language='nb-NO')
        response.pause(length=60)  # Hold linjen åpen

        return str(response)

    # =========================================================================
    # SMS SENDING
    # =========================================================================

    def _send_emergency_sms(self, contact_keys: List[str], message: str):
        """Send SMS til spesifiserte kontakter"""
        for key in contact_keys:
            contact = self.contacts.get(key)
            if not contact:
                logger.warning(f"⚠️ Contact {key} not found")
                continue

            if self.test_mode:
                logger.info(f"📱 TEST: Would SMS {contact.name} ({contact.phone}): {message}")
                continue

            if not self.twilio_client:
                logger.error("❌ Twilio not configured for SMS")
                continue

            try:
                self.twilio_client.messages.create(
                    to=contact.phone,
                    from_=self.twilio_number,
                    body=message
                )
                logger.info(f"📱 SMS sent to {contact.name}")
            except Exception as e:
                logger.error(f"❌ Failed to send SMS to {contact.name}: {e}")

    # =========================================================================
    # HOME ASSISTANT
    # =========================================================================

    def _trigger_ha_scene(self, scene_name: str):
        """Trigger en HA scene"""
        if not self.ha_token:
            logger.warning("⚠️ HA token not configured")
            return

        if self.test_mode:
            logger.info(f"🏠 TEST: Would trigger HA scene '{scene_name}'")
            return

        try:
            url = f"{self.ha_url}/api/services/scene/turn_on"
            headers = {
                "Authorization": f"Bearer {self.ha_token}",
                "Content-Type": "application/json"
            }
            data = {"entity_id": f"scene.{scene_name}"}

            response = requests.post(url, headers=headers, json=data, timeout=5)
            if response.ok:
                logger.info(f"🏠 HA scene '{scene_name}' triggered")
            else:
                logger.error(f"❌ HA error: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ HA connection failed: {e}")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def is_emergency_request(text: str) -> bool:
    """Sjekk om brukeren ber om nødhjelp"""
    emergency_keywords = [
        "ring 113", "ring ambulanse", "trenger ambulanse",
        "ring politiet", "ring 112", "nødsituasjon",
        "har skadet meg", "trenger hjelp", "ring etter hjelp"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in emergency_keywords)


def is_confirmation(text: str) -> bool:
    """Sjekk om brukeren bekrefter"""
    confirmations = [
        "ja", "ja ring", "ring nå", "ja ring nå",
        "bekreft", "gjør det", "ja gjør det"
    ]
    text_lower = text.lower().strip()
    return any(conf in text_lower for conf in confirmations)


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("🚨 Testing Emergency System")
    print("=" * 50)

    # Opprett system
    em = EmergencySystem()

    # Test distress phrases
    test_phrases = [
        "Hei General, husk å mate katten i morgen",
        "Hei General, hva er klokka?",
        "Hei General, hvor mye koster den hvite malingen?",
        "General, jeg har skadet meg og trenger ambulanse"
    ]

    for phrase in test_phrases:
        print(f"\n📝 Testing: '{phrase}'")

        # Sjekk distress
        distress = em.check_distress_phrase(phrase)
        if distress:
            print(f"   🚨 DISTRESS: {distress['type']}")
            response = em.handle_distress(distress)
            print(f"   💬 Response: {response}")
        elif is_emergency_request(phrase):
            print(f"   🆘 EXPLICIT EMERGENCY REQUEST")
            response = em.request_emergency_call(phrase)
            print(f"   💬 Response: {response}")
        else:
            print(f"   ✅ Normal phrase")

    print("\n" + "=" * 50)
    print("✅ Test complete!")
