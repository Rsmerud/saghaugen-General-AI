# Sweet Home 3D - Oppsett for Saghaugen

## Steg 1: Start Sweet Home 3D

```bash
sweethome3d &
```

Eller søk etter "Sweet Home 3D" i applikasjonsmenyen.

## Steg 2: Importer bakgrunnskart

1. Gå til **Plan > Import background image...**
2. Velg filen: `/home/ronny/ClaudeCodeProjects/GeneralAI/saghaugen/kart/flyfoto_saghaugen.png`
3. **VIKTIG - Sett målestokk:**
   - Finn målestokk-linjen (10m) nederst til venstre i bildet
   - Klikk på starten av 10m-linjen
   - Klikk på slutten av 10m-linjen
   - Skriv inn "1000" cm (10 meter = 1000 cm)
4. Juster origin point om ønskelig
5. Klikk **Finish**

## Steg 3: Tegn tomtegrense

1. Velg **Create rooms** verktøyet (eller trykk `R`)
2. Tegn langs den røde tomtegrensen i kartet
3. Dobbeltklikk for å lukke formen

## Steg 4: Tegn bygninger

### Hovedhus (~9m x 8m)
1. Velg **Create rooms**
2. Tegn omrisset av hovedhuset
3. Høyreklikk > **Modify room** > Sett navn til "Hovedhus"

### Låve (~13m x 10m)
1. Tegn omrisset av låven
2. Høyreklikk > **Modify room** > Sett navn til "Låve"

## Steg 5: Legg til planlagte elementer

Bruk **Furniture**-katalogen til venstre:
- **Exterior > Garden** - Planter, trær, busker
- **Exterior > Vehicles** - For å vise parkering/carport
- **Miscellaneous** - Diverse objekter

### Plasseringer å vurdere:
- **Drivhus:** Sør-vendt, nær kjøkkenhage
- **Hønegård:** Litt unna huset, men tilgjengelig
- **Carport:** Ved innkjørselen
- **Potetland:** Solrikt område

## Steg 6: Lagre prosjektet

1. **File > Save as...**
2. Lagre til: `/home/ronny/ClaudeCodeProjects/GeneralAI/saghaugen/sweet-home-3d/saghaugen.sh3d`

## Tips

- **3D-visning:** Trykk på 3D-fanen nederst for å se landskapet i 3D
- **Zoom:** Scroll for å zoome inn/ut
- **Pan:** Hold mellomknappen og dra
- **Målinger:** Bruk linjalen i verktøylinjen

## Målreferanser

Basert på kartet (10m målestokk):
- Avstand hovedhus til låve: ~25-30m
- Tomtebredde (øst-vest): ~100m
- Tomtelengde (nord-sør): ~120m
- Total tomt: ~7000 kvm (7 mål)
