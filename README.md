# ehealth-implementation.eu

Webbplats för Interreg South Baltic-projektet **AMBeR – Advanced Modeling of Baltic Cancer E-Care**.
Sidans innehåll är på engelska.

## Så fungerar det

- Allt innehåll ligger som textfiler (Markdown) i `src/content/`.
- När en ändring sparas på grenen `main` bygger GitHub automatiskt om webbplatsen och publicerar den på GitHub Pages (tar ett par minuter).
- Ingen databas, inga cookies och ingen server att underhålla.

## Redigera innehåll (utan kod)

1. Gå till <https://app.pagescms.org> och logga in med ert GitHub-konto.
2. Välj repot `IoU-Angelhaven/ehealth-implementation` och grenen `main`.
3. I menyn till vänster finns: **Model – Phases**, **Model – Activities**, **Stories** och de enskilda sidorna (**Page – …**).
4. Ändra texten och klicka **Save**. Ändringen sparas direkt på `main` och webbplatsen uppdateras automatiskt efter ett par minuter.

Bra att veta:

- **Berättelser (Stories):** välj fas och ikon i formuläret. Stäng av **Published** för att dölja en berättelse.
- **Nedladdningar:** filer laddas upp i fältet "Download (upload a file)" – på sidan *Create your local guide* (PDF och Word av hela guiden) och på *Learnings & resources*. Tills en fil finns visas "coming soon".
- **Filnamn:** använd korta namn utan mellanslag och utan å, ä, ö.
- Bilder och dokument som laddas upp via editorn hamnar i `public/media/`.
- Allt innehåll skrivs på brittisk engelska (organisation, programme, centre).

## Sidor

| Sida | Adress | Innehåll redigeras i |
|---|---|---|
| Home | `/` | Page – Home |
| The implementation model | `/model/` | Page – The implementation model, Model – Phases, Model – Activities |
| Stories | `/stories/` | Stories |
| Learnings & resources | `/resources/` | Page – Learnings & resources |
| Create your local guide | `/local-guide/` | Page – Create your local guide |
| About AMBeR | `/about/` | Page – About AMBeR |
| Privacy | `/privacy/` | Page – Privacy |
| Accessibility | `/accessibility/` | Page – Accessibility |
| AI usage in development | `/ai-usage/` | Page – AI usage in development |

## Var ligger vad?

| Innehåll | Mapp |
|---|---|
| Modellens 5 faser | `src/content/steps/` (en fil per fas: `step-1.md` … `step-5.md`) |
| Modellens 30 aktiviteter | `src/content/activities/` (en fil per aktivitet) |
| Stories | `src/content/stories/` |
| Startsida, About, Local guide, Resources, Privacy, Accessibility, AI usage | `src/content/pages/` |
| Färger och typsnitt | `src/styles/global.css` |
| Ikoner (namnen går att välja i editorn) | `src/icons.ts` |
| Menyn, sajtens namn, kontaktadress, statistik | `src/site.config.ts` |
| Bilder och nedladdningsbara filer | `public/media/` |
| Officiella logotyper (ändra inte) | `public/media/brand/` |

Filnamnen `step-1` … `step-5` och aktiviteternas filnamn används i webbadresserna. Byt inte namn på dem.

## Kvar att göra innan lansering

- **Privacy** och **Accessibility** innehåller platshållartext som ska ersättas (bl.a. vem som är personuppgiftsansvarig och hur man rapporterar tillgänglighetsbrister).
- **Learnings & resources** har tre platshållarkort.
- Åtta berättelser är utkast med text i [hakparentes] som ska kompletteras av respektive organisation.
- Filerna för nedladdning (PDF och Word) är inte uppladdade.
- Kontaktadress (`contactEmail`) och besöksstatistik (`analytics`) är inte ifyllda i `src/site.config.ts`.
- Ingen licens är vald för innehållet (t.ex. CC BY 4.0).

## Interregs regler som webbplatsen följer

Enligt *Communication Guidelines for Beneficiaries* (Interreg South Baltic, v.6):

- Logotypen (AMBeR + Interreg South Baltic + EU) ligger överst på varje sida, på vit bakgrund och i föreskriven minsta storlek.
- Finansieringstexten och ansvarsfriskrivningen står i sidfoten med programmets formulering.
- Sidan *About* beskriver projektets mål, resultat, partner, period, budget/EU-stöd och målgrupper.
- Typsnittet är Open Sans.
- Projektnamnet skrivs som i logotypen: *Advanced Modeling of Baltic Cancer E-Care*.
- Webbplatsen ska hållas uppdaterad och finnas kvar minst under projektets livstid. Riktlinjerna avråder från att publicera en halvfärdig webbplats.

## Större ändringar

Struktur, design och nya funktioner kan ni be Claude om (på svenska). Ändringarna görs då på en separat gren
och slås ihop med `main` via en pull request när ni har godkänt dem. Slå ihop en pull request först när alla
ändringar ni väntar på är med – det som läggs till efteråt behöver en ny pull request.

## Publicering

Webbplatsen publiceras på två ställen:

- **GitHub Pages (förhandsvisning):** byggs och publiceras automatiskt varje gång något sparas på grenen `main`. Adressen är <https://iou-angelhaven.github.io/amber/>.
- **Loopia (den riktiga adressen):** <https://amber.ehealth-implementation.eu>. Publiceras bara när någon trycker på knappen, se nedan.

**GitHub Pages: inställning som måste vara rätt (görs en gång):**
GitHub → repot → *Settings* → *Pages* → *Build and deployment* → *Source*: välj **GitHub Actions**.
(Välj *inte* "Deploy from a branch" – då försöker GitHub visa källkoden i stället för den färdiga webbplatsen.)
Om publiceringen misslyckas: gå till fliken *Actions*, öppna "Build and publish website" och klicka *Re-run jobs*.

**Loopia: publicera för hand**
1. Fliken *Actions* → **Publish to Loopia (amber.ehealth-implementation.eu)** → *Run workflow*.
2. Välj först **Dry run**. Den loggar in hos Loopia och visar vilka filer som skulle laddas upp och tas bort, utan att ändra något.
3. Ser det rätt ut: kör igen och välj **Publish**. Ändringen syns på amber.ehealth-implementation.eu efter en kort stund (Loopias cache).

Inloggningen till Loopia ligger som hemligheterna `FTP_USER` och `FTP_PASS` (*Settings* → *Secrets and variables* → *Actions*). FTP-kontot når bara AMBeR:s mapp hos Loopia. Lösenord skrivs aldrig i filer, commits eller chatt.

Huvudadressen ehealth-implementation.eu ska inte pekas till GitHub Pages: den blir den gemensamma plattformens ingång (se plattformens repo, `docs/LOOPIA-TAGORDNING.md`).

## För utvecklare

```bash
npm install
npm run dev      # lokal förhandsvisning på http://localhost:4321/ehealth-implementation/
npm run build    # bygger till dist/
```

`npm run build` skapar också `sitemap.xml` och `robots.txt`. Kör `npm audit` då och då för att se om byggverktygen har kända säkerhetsbrister.

Byggt med [Astro](https://astro.build). Innehållsscheman finns i `src/content.config.ts`, redigeringsgränssnittet konfigureras i `.pages.yml`.
