# Erzeugt die englischen Blöcke (#en, #en-leicht) aus den deutschen Blöcken der Arbeitsdatei.
# Aufruf: python3 englisch.py <arbeitsdatei.html>
# Die englischen Blöcke stehen zwischen <!-- EN:START --> und <!-- EN:END --> und werden bei jedem Lauf neu erzeugt.
import re, sys, html

T = {
 # Umschalter / allgemein
 "Zum Inhalt springen": "Skip to content", "Kreativ": "Creative", "Leichte Sprache": "Easy Read",
 "Ballett ✦ Modern Dance ✦ Arbeit mit Kindern ✦ Inklusion ✦ Zeichnen ✦ Gesang ✦ Make-up ✦ Fotoshootings ✦ Gestaltung ✦": "Ballet ✦ Modern Dance ✦ Working with Children ✦ Inclusion ✦ Drawing ✦ Singing ✦ Make-up ✦ Photo Shoots ✦ Design ✦",
 "Schrift": "Text size", "A": "A", "A+": "A+", "Schriftgröße": "Text size",
 "Bühne frei für": "Stage clear for", "Anouk": "Anouk",
 "auch „Kuna“ genannt": "also known as “Kuna”",
 "Beispiel": "Example", "Beispieltext": "Sample text", "Platzhalter": "Placeholder",
 "In Bewegung. Mit Ideen. Und ganz viel Neugier.": "In motion. With ideas. And a lot of curiosity.",
 "Tanz. Ausdruck. Kreativität. Und ein großes Herz für Menschen.": "Dance. Expression. Creativity. And a big heart for people.",
 "Tänzerin in Ausbildung mit den Schwerpunkten Ballett und Modern Dance. Genauso gern arbeite ich mit Kindern und mit Menschen mit Behinderung, auf der Bühne und im Alltag.": "Dancer in training with a focus on ballet and modern dance. I love working with children and with people with disabilities just as much, on stage and in everyday life.",
 "Offen für Engagements, Auditions und Stellen in der Betreuung": "Open to engagements, auditions and care work",
 "Kontakt aufnehmen": "Get in touch", "Programm ansehen": "See the programme",
 "Hier sollte ein Porträtfoto sein.": "A portrait photo should go here.",
 "Platzhalter für ein Porträtfoto von Anouk, mit einer geschwungenen roten Linie als Zeichnung": "Placeholder for a portrait photo of Anouk, with a sweeping red line as a drawing",
 "Der Vorhang öffnet sich beim Betreten der Seite.": "The curtain opens when you enter the page.",
 "Noch einmal": "Once more",
 # Programm
 "Programm": "Programme", "Prolog": "Prologue", "Das bin ich": "This is me",
 "Akt I": "Act I", "Meine Leidenschaft": "My Passion", "Akt II": "Act II", "Mein Weg": "My Path",
 "Akt III": "Act III", "Fähigkeiten und Möglichkeiten": "Skills and Possibilities",
 "Akt IV": "Act IV", "Meine kreative Welt": "My Creative World", "Finale": "Finale", "Kontakt": "Contact",
 "Reihe 1, Platz 1": "Row 1, Seat 1", "Spieldauer": "Running time", "ca. 4 Minuten": "approx. 4 minutes",
 "Pause": "Interval", "keine": "none", "Eintritt": "Admission", "frei": "free", "Programm ↑": "Programme ↑",
 "Schnell zu den Akten": "Jump to the acts",
 # Prolog
 "Ich bin Anouk, viele nennen mich Kuna. Mein Weg ist geprägt von Neugier, dem Wunsch nach Weiterentwicklung und der Freude daran, Menschen zu erreichen.": "I am Anouk, many people call me Kuna. My path is shaped by curiosity, the wish to keep growing and the joy of reaching people.",
 "Das gelingt mir durch Kunst und Bewegung, genauso aber im ganz normalen Alltag. Neben meiner Tanzausbildung arbeite ich gern mit Kindern und mit Menschen mit Behinderung. Das kann auf der Bühne sein, in einer Kita, einer Schule oder einer Wohngruppe.": "I do that through art and movement, but just as much in everyday life. Alongside my dance training I love working with children and with people with disabilities. That can be on stage, in a nursery, a school or a residential group.",
 "Extravagant.": "Extravagant.", "Individuell.": "Individual.", "Außergewöhnlich.": "Extraordinary.",
 "Mein Stil: extravagant, individuell, außergewöhnlich": "My style: extravagant, individual, extraordinary",
 "So beschreibe ich meinen Stil, auf der Bühne wie im Alltag: gut gekleidet, gepflegt und nie langweilig. Vor der Kamera fühle ich mich wohl. Ich liebe künstlerische Fotoshootings und ausdrucksstarke Inszenierungen.": "That is how I describe my style, on stage and in everyday life: well dressed, well groomed and never boring. I feel at home in front of the camera. I love artistic photo shoots and expressive staging.",
 "Hier sollte ein persönlicher Vorstellungstext stehen.": "A personal introduction should go here.",
 "Mein Backstage-Pass, alles auf einen Blick": "My backstage pass, everything at a glance",
 "Backstage": "Backstage", "All Access": "All Access", "„Kuna“": "“Kuna”",
 "Backstage-Pass: Profil auf einen Blick": "Backstage pass: profile at a glance",
 "Rolle": "Role", "Tänzerin in Ausbildung": "Dancer in training", "Stilrichtungen": "Styles", "Ballett, Modern Dance": "Ballet, modern dance",
 "Ausbildung": "Training", "Tanzakademie am Lindenhof, seit 2023 weiterführend": "Lindenhof Dance Academy, advanced training since 2023",
 "Herzensthema": "Close to my heart", "Kinder und Menschen mit Behinderung": "Children and people with disabilities",
 "Zeichnen, Gesang, Make-up, Fotoshootings, Gestaltung": "Drawing, singing, make-up, photo shoots, design",
 "Markenzeichen": "Trademark", "Intensiver Blick, eigener Stil": "Intense gaze, a style of my own",
 "Stärken": "Strengths", "Kreativität, Ehrgeiz, Reflexion, Interesse an Menschen": "Creativity, ambition, reflection, interest in people",
 # Akt I
 "Einzählen: fünf, sechs, sieben, acht": "Counting in: five, six, seven, eight", "und los!": "and go!",
 "Tanz ist für mich mehr als Bewegung. Er verbindet Technik, Ausdruck, Kreativität und die Möglichkeit, sich immer wieder neu zu entdecken.": "For me, dance is more than movement. It combines technique, expression, creativity and the chance to discover myself anew, again and again.",
 "Ballett": "Ballet", "Technik, Haltung und Präzision. Hier lerne ich, jede Bewegung bewusst zu setzen.": "Technique, posture and precision. This is where I learn to place every movement deliberately.",
 "Modern Dance": "Modern dance", "Raum für Ausdruck und eine eigene Bewegungssprache, mit dem Boden als Partner.": "Room for expression and a movement language of my own, with the floor as a partner.",
 "Hier sollte ein Text stehen: Was bedeutet Tanz für mich?": "A text should go here: What does dance mean to me?",
 "Tanzfotografie": "Dance photography", "Hier sollte ein Tanzfoto sein.": "A dance photo should go here.",
 "Platzhalter Tanzfoto 1, Großansicht öffnen": "Placeholder dance photo 1, open large view",
 "Platzhalter Tanzfoto 2, Großansicht öffnen": "Placeholder dance photo 2, open large view",
 "Platzhalter Tanzfoto 3, Großansicht öffnen": "Placeholder dance photo 3, open large view",
 "Hier könnte ein Showreel oder Auftrittsvideo sein.": "A showreel or performance video could go here.",
 "Auftritte und Projekte": "Performances and projects",
 "„Zwischen den Zeilen“": "“Between the Lines”", "· Solo im Modern Dance, Abschlussabend, 2023": "· modern dance solo, graduation evening, 2023",
 "„Alle an Bord“": "“All Aboard”", "· Inklusives Tanzprojekt mit Kindern, 2022": "· inclusive dance project with children, 2022",
 "„Schneeflockenwalzer“ aus „Der Nussknacker“": "“Waltz of the Snowflakes” from “The Nutcracker”", "· Ensemble, 2021": "· ensemble, 2021",
 "Sedcard: Daten für Auditions": "Sedcard: audition data",
 "Größe": "Height", "— cm": "— cm", "Konfektionsgröße": "Dress size", "Schuhgröße": "Shoe size", "Haarfarbe": "Hair colour", "Augenfarbe": "Eye colour",
 "Tanzstile": "Dance styles", "Sprachen": "Languages", "Deutsch, —": "German, —",
 "Hier sollten die echten Maße und Angaben stehen.": "The real measurements and details should go here.",
 "Hier sollten die eigenen Auftritte, Projekte und Workshops stehen. Die Einträge oben sind Beispiele.": "The real performances, projects and workshops should go here. The entries above are examples.",
 # Akt II
 "Tanz": "Dance", "Arbeit mit Menschen": "Working with people",
 "seit 2023": "since 2023", "Weiterführende Tanzausbildung": "Advanced dance training", "Aktuell": "Current",
 "Vertiefung in Ballett und Modern Dance": "Deepening ballet and modern dance",
 "Solo im Modern Dance, Abschlussabend": "Modern dance solo, graduation evening",
 "seit 2022": "since 2022", "Mitarbeit in einer Praxis": "Work in a medical practice",
 "Empfang und Organisation, täglicher Kontakt mit Menschen in ganz unterschiedlichen Lebenslagen": "Reception and organisation, daily contact with people in very different situations",
 "Inklusives Projekt mit Kindern, Anleitung von Kindergruppen": "Inclusive project with children, leading children’s groups",
 "Ensemble": "Ensemble", "Professionelle Tanzausbildung": "Professional dance training",
 "Tanzakademie am Lindenhof, Schwerpunkte Ballett und Modern Dance": "Lindenhof Dance Academy, focus on ballet and modern dance",
 "Hier sollten die echten Stationen stehen: Ausbildung, Arbeit, Projekte. Die Einträge oben sind Beispiele.": "The real stages should go here: training, work, projects. The entries above are examples.",
 # Akt III
 "Tanz und die Arbeit mit Menschen gehören für mich zusammen. Ich muss mich nicht für eine Bühne entscheiden, beide stehen mir offen, gern auch gleichzeitig.": "For me, dance and working with people belong together. I do not have to choose one stage; both are open to me, happily at the same time.",
 "Was ich mitbringe": "What I bring",
 "Kreativität": "Creativity", "Ich entwickle eigene Bewegungsideen und finde für jede Gruppe einen passenden Zugang.": "I develop my own movement ideas and find the right approach for every group.",
 "Ehrgeiz": "Ambition", "Ich trainiere diszipliniert und arbeite an jedem Detail, bis es sitzt.": "I train with discipline and work on every detail until it is right.",
 "Reflexionsfähigkeit": "Reflection", "Ich nehme Feedback an, frage nach und setze es in der nächsten Probe um.": "I take feedback on board, ask questions and apply it in the next rehearsal.",
 "Interesse an Menschen": "Interest in people", "Ich sehe, was jemand kann, und helfe dabei, den nächsten Schritt zu gehen.": "I see what someone can do and help them take the next step.",
 "Stimmen": "Voices",
 "Hier könnte ein kurzes Zitat stehen, zum Beispiel von einer Lehrkraft, einer Choreografin oder Eltern. Nur mit Einverständnis der Person.": "A short quote could go here, for example from a teacher, a choreographer or parents. Only with the person’s consent.",
 "Hier könnte ein zweites Zitat stehen.": "A second quote could go here.",
 "Zwei Bühnen, beide offen": "Two stages, both open",
 "Bühne 1": "Stage 1", "Kompanie, Theater und Tanzvermittlung": "Company, theatre and dance education",
 "Klassische Basis aus dem Ballett, Ausdruckskraft aus dem Modern Dance, Bühnenerfahrung im Ensemble und solistisch. Dazu Gesang, Bühnen-Make-up, Präsenz vor Publikum und Kamera, Skizzen für Kostüme und Bühnenbilder und Freude daran, Tanz weiterzugeben.": "A classical foundation from ballet, expressiveness from modern dance, stage experience in an ensemble and as a soloist. Plus singing, stage make-up, presence in front of an audience and the camera, sketches for costumes and sets, and the joy of passing dance on.",
 "Passt zu": "Suits", "Tanzkompanien und Theater": "Dance companies and theatres", "Theaterpädagogik und Junges Haus": "Theatre education and youth programmes", "Tanz- und Musikschulen": "Dance and music schools",
 "Für": "For", "Ballettdirektion": "Ballet directors", "Kompanieleitung": "Company managers", "Leitung Theaterpädagogik": "Heads of theatre education", "Schulleitung": "School heads",
 "Bühne 2": "Stage 2", "Menschen": "People", "Begleitung von Kindern und Menschen mit Behinderung": "Supporting children and people with disabilities",
 "Auch abseits des Tanzens arbeite ich gern mit Menschen, die Begleitung brauchen. Ich bringe Geduld mit, Ideen für kreative Angebote mit Musik, Bewegung, Zeichnen und Gestaltung und Erfahrung darin, Gruppen anzuleiten.": "Away from dance, too, I love working with people who need support. I bring patience, ideas for creative activities with music, movement, drawing and design, and experience in leading groups.",
 "Kitas und Horte": "Nurseries and after-school care", "Schulbegleitung und Ganztag": "School support and all-day programmes", "Wohngruppen, Tagesstätten und Werkstätten": "Residential groups, day centres and workshops", "Freizeit- und Ferienangebote": "Leisure and holiday programmes",
 "Kita-Leitung": "Nursery managers", "Einrichtungsleitung": "Facility managers", "Träger der Eingliederungshilfe": "Disability support providers",
 "… oder beides zugleich. Ich bin offen für Wege, die es noch nicht gibt.": "… or both at once. I am open to paths that do not exist yet.",
 # Akt IV
 "Wenn ich nicht tanze, zeichne ich. Skizzen helfen mir, Bewegung festzuhalten, Ideen für Kostüme und Shootings zu entwickeln und mit Kindern ins Gestalten zu kommen.": "When I am not dancing, I draw. Sketches help me capture movement, develop ideas for costumes and shoots, and get children into making things.",
 "Zeichnen": "Drawing", "Bewegungsskizzen, Figuren und Kostümideen.": "Movement sketches, figures and costume ideas.",
 "Gesang": "Singing", "Singen gehört für mich zur Bühne dazu.": "For me, singing is part of the stage.",
 "Maske": "Make-up", "Bühnen-Make-up und Looks, von natürlich bis extravagant.": "Stage make-up and looks, from natural to extravagant.",
 "Gestaltung": "Design", "Requisiten, Plakate und kleine Bühnenbilder.": "Props, posters and small stage sets.",
 "Fotoshooting": "Photo shoots", "Künstlerische Shootings und ausdrucksstarke Inszenierungen.": "Artistic shoots and expressive staging.",
 "Styling": "Styling", "Gut gekleidet, gepflegt und nie langweilig.": "Well dressed, well groomed and never boring.",
 "Galerie: eigene Arbeiten": "Gallery: my own work", "Zeichnungen, Kostümideen, Fotos von Projekten. Zum Vergrößern anklicken.": "Drawings, costume ideas, photos of projects. Click to enlarge.",
 "Hier sollte eine Zeichnung sein.": "A drawing should go here.", "Hier sollte eine Kostümidee oder ein Projekt sein.": "A costume idea or a project should go here.", "Hier sollte ein Bild aus einem Fotoshooting sein.": "A picture from a photo shoot should go here.",
 "Platzhalter Zeichnung 1, Großansicht öffnen": "Placeholder drawing 1, open large view", "Platzhalter Zeichnung 2, Großansicht öffnen": "Placeholder drawing 2, open large view",
 "Platzhalter Kostümidee, Großansicht öffnen": "Placeholder costume idea, open large view", "Platzhalter Fotoshooting, Großansicht öffnen": "Placeholder photo shoot, open large view",
 "Zeichnen Sie mit!": "Draw along!", "Stiftfarbe": "Pen colour", "Rot": "Red", "Gelb": "Yellow", "Grün": "Green", "Tinte": "Ink",
 "Skizze speichern": "Save sketch", "Neu anfangen": "Start over",
 "Zeichenfläche: mit Maus, Finger oder Stift zeichnen": "Drawing area: draw with mouse, finger or pen",
 "Ihre Skizze bleibt nur hier auf Ihrem Bildschirm und wird nicht gespeichert.": "Your sketch stays on your screen only and is not stored anywhere.",
 # Finale
 "Ich freue mich auf Ihre": "I look forward to your", "Nachricht.": "message.",
 "Ob Audition, Hospitation, Projekt oder einfach ein Gespräch: Schreiben Sie mir. Lebenslauf und Zeugnisse sende ich gern zu.": "Audition, work shadowing, a project or simply a conversation: write to me. I am happy to send my CV and references.",
 "Bühneneingang": "Stage door", "hallo@anouk-dance.example": "hallo@anouk-dance.example", "Adresse kopieren": "Copy address",
 "Hier sollte die echte E-Mail-Adresse stehen. Diese ist nur ein Beispiel.": "The real e-mail address should go here. This one is only an example.",
 "Hier könnte ein Download-Paket sein: Lebenslauf, Sedcard und zwei bis drei Fotos als PDF.": "A download package could go here: CV, sedcard and two or three photos as a PDF.",
 "Hier könnten weitere Kontaktwege oder Profile stehen. Keine Adresse, keine Telefonnummer.": "Further ways to get in touch or profiles could go here. No postal address, no phone number.",
 "Vorhang.": "Curtain.",
 "© 2026 Anouk · Dance &amp; Creative Arts. Diese Seite verzichtet bewusst auf Adresse, Telefonnummer und Geburtsdatum.": "© 2026 Anouk · Dance &amp; Creative Arts. This page deliberately leaves out postal address, phone number and date of birth.",
 "Zur Version in Leichter Sprache": "Easy Read version", "Zum Programm": "To the programme", "Impressum": "Legal notice (German)", "Datenschutz": "Privacy (German)",
 "Schließen": "Close", "Großansicht": "Large view",
 # Easy Read
 "Ich bin Anouk.": "I am Anouk.", "Ich tanze.": "I dance.", "Und ich arbeite gern mit Menschen.": "And I like working with people.",
 "Diese Seite ist in Leichter Sprache.": "This page is written in easy English.", "Die Sätze sind kurz.": "The sentences are short.", "Schwere Wörter werden erklärt.": "Difficult words are explained.",
 "Es gibt keine Bewegung auf dieser Seite.": "Nothing moves on this page.",
 "Diese Seite soll für alle gut lesbar sein. Fachleute haben das noch nicht geprüft.": "This page should be easy to read for everyone. Experts have not checked it yet.",
 "Diese Seite ist noch ein Entwurf.": "This page is still a draft.",
 "Manche Angaben sind nur Beispiele. Sie sind so markiert:": "Some details are only examples. They are marked like this:",
 "Das ist ein Beispiel.": "This is an example.", "An manchen Stellen ist Platz für eigene Inhalte. Sie sind so markiert:": "In some places there is room for her own content. They are marked like this:",
 "Das ist ein Platzhalter.": "This is a placeholder.", "Manche Sätze sind Beispiel-Texte. Sie sind so markiert:": "Some sentences are sample texts. They are marked like this:",
 "Das ist ein Beispiel-Text.": "This is a sample text.",
 "Inhalt dieser Seite": "Contents of this page", "Seite anpassen": "Adjust the page", "Wer ich bin": "Who I am", "Tanzen": "Dancing", "Was ich kann und möchte": "What I can do and want",
 "Meine Bilder": "My pictures", "Sie können die Seite anpassen": "You can adjust the page", "Schrift-Größe": "Text size",
 "Normal": "Normal", "Groß": "Large", "Sehr groß": "Very large", "Farben": "Colours", "Schwarz auf Weiß": "Black on white", "Gelb auf Schwarz": "Yellow on black",
 "Vorlesen": "Read aloud", "Text vorlesen": "Read the text aloud", "Der Computer liest den Text laut vor. Das geht nicht auf jedem Gerät.": "The computer reads the text aloud. This does not work on every device.",
 "Ich heiße Anouk.": "My name is Anouk.", "Meine Freunde nennen mich Kuna.": "My friends call me Kuna.", "Ich bin Tänzerin.": "I am a dancer.",
 "Ich mache gerade eine Tanz-Ausbildung.": "I am doing dance training right now.", "Ich tanze": "I dance", "und": "and",
 "Ich bin in Bewegung. Ich habe Ideen. Und ich bin neugierig.": "I am in motion. I have ideas. And I am curious.",
 "Was bedeuten die Wörter?": "What do the words mean?",
 "ist ein klassischer Tanz. Die Tänzer tanzen zu Musik. Die Bewegungen haben feste Regeln.": "is a classical dance. The dancers dance to music. The movements follow fixed rules.",
 "heißt: moderner Tanz. Man bewegt sich frei. Man zeigt Gefühle mit dem Körper.": "means: modern dancing. You move freely. You show feelings with your body.",
 "Ich zeichne gern.": "I like drawing.", "Ich singe gern.": "I like singing.", "Ich schminke gern. Zum Beispiel für die Bühne.": "I like doing make-up. For example for the stage.",
 "Ich stehe gern vor der Kamera. Ich mache gern Foto-Shootings.": "I like being in front of the camera. I like photo shoots.",
 "Ich ziehe mich gern besonders an. Mein Stil ist auffällig. Und immer gepflegt.": "I like dressing in a special way. My style stands out. And it is always neat.",
 "Hier sollte ein persönlicher Text stehen.": "A personal text should go here.", "Hier sollte ein Foto sein.": "A photo should go here.",
 "Tanzen ist für mich mehr als Bewegung.": "For me, dancing is more than movement.", "Beim Tanzen zeige ich, was ich fühle.": "When I dance, I show what I feel.", "Ich lerne jeden Tag etwas Neues.": "I learn something new every day.",
 "Hier sollte ein Text stehen: Was bedeutet Tanzen für mich?": "A text should go here: What does dancing mean to me?",
 "Hier sollten Fotos vom Tanzen sein. Vielleicht auch ein Video.": "Photos of dancing should go here. Maybe a video, too.",
 "Meine Maße": "My measurements", "Größe: — cm": "Height: — cm", "Kleider-Größe: —": "Dress size: —", "Schuh-Größe: —": "Shoe size: —", "Haar-Farbe: —": "Hair colour: —", "Augen-Farbe: —": "Eye colour: —",
 "Auftritte": "Performances",
 "2023: Ich habe ein Solo getanzt. Ein Solo heißt: Man tanzt allein auf der Bühne.": "2023: I danced a solo. A solo means: you dance alone on stage.",
 "2022: Ich habe beim Projekt „Alle an Bord“ mitgemacht. Das war ein Tanz-Projekt mit Kindern. Mit und ohne Behinderung.": "2022: I took part in the project “All Aboard”. It was a dance project with children. With and without disabilities.",
 "2021: Ich habe im Ballett „Der Nussknacker“ getanzt.": "2021: I danced in the ballet “The Nutcracker”.",
 "2019 bis 2023:": "2019 to 2023:", "Tanz-Ausbildung an der Tanz-Akademie am Lindenhof.": "Dance training at the Lindenhof Dance Academy.",
 "Seit 2022:": "Since 2022:", "Ich arbeite in einer Praxis. Am Empfang. Ich spreche jeden Tag mit vielen Menschen.": "I work in a medical practice. At the reception. I talk to many people every day.",
 "Seit 2023:": "Since 2023:", "Ich lerne weiter. Ich mache eine weitere Tanz-Ausbildung.": "I keep learning. I am doing further dance training.",
 "Hier sollten die echten Stationen stehen. Die Sätze oben sind nur Beispiele.": "The real stages should go here. The sentences above are only examples.",
 "Ich habe viele Ideen.": "I have many ideas.", "Ich arbeite viel. Ich gebe nicht auf.": "I work hard. I do not give up.",
 "Ich denke über meine Arbeit nach. Ich frage: Was kann ich besser machen?": "I think about my work. I ask: What can I do better?", "Ich interessiere mich für Menschen. Ich helfe gern.": "I am interested in people. I like to help.",
 "Ich suche Arbeit.": "I am looking for work.", "Ich kann zwei Dinge gut. Ich muss mich nicht entscheiden. Beides geht auch zusammen.": "I am good at two things. I do not have to choose. Both work together, too.",
 "1. Tanzen": "1. Dancing", "Ich möchte in einer Tanz-Gruppe tanzen. Zum Beispiel in einem Theater.": "I would like to dance in a dance company. For example in a theatre.",
 "Oder ich zeige anderen Menschen das Tanzen. Zum Beispiel Kindern in einer Tanz-Schule.": "Or I teach other people to dance. For example children in a dance school.",
 "2. Mit Menschen arbeiten": "2. Working with people", "Ich möchte Kinder betreuen.": "I would like to look after children.", "Oder ich möchte Menschen mit Behinderung begleiten.": "Or I would like to support people with disabilities.",
 "Zum Beispiel in einer Kita. Oder in einer Schule. Oder in einer Wohn-Gruppe.": "For example in a nursery. Or in a school. Or in a residential group.",
 "Ich habe Geduld. Und ich habe viele Ideen. Zum Beispiel mit Musik, Bewegung und Malen.": "I am patient. And I have many ideas. For example with music, movement and painting.",
 "Sie leiten ein Theater, eine Schule oder eine Einrichtung?": "Do you run a theatre, a school or a care facility?", "Dann schreiben Sie mir gern.": "Then please write to me.",
 "Ich zeichne gern. Zum Beispiel Menschen in Bewegung. Oder Ideen für Kostüme.": "I like drawing. For example people in motion. Or ideas for costumes.",
 "Hier sollten Bilder von Zeichnungen sein.": "Pictures of drawings should go here.",
 "In der kreativen Version gibt es eine Zeichen-Fläche. Dort können Sie selbst malen.": "The creative version has a drawing area. You can draw there yourself.",
 "Schreiben Sie mir eine E-Mail.": "Write me an e-mail.", "Ich freue mich über Ihre Nachricht.": "I look forward to your message.", "Ich schicke Ihnen gern meinen Lebenslauf.": "I am happy to send you my CV.",
 "Meine E-Mail-Adresse:": "My e-mail address:", "Hier könnte ein Knopf sein: Lebenslauf, Maße und Fotos herunterladen.": "A button could go here: download CV, measurements and photos.",
 "Auf dieser Seite steht keine Adresse. Und keine Telefon-Nummer.": "There is no postal address on this page. And no phone number.", "Das ist Absicht. So schütze ich meine Daten.": "That is on purpose. This is how I protect my data.",
 "Die andere Version": "The other version", "Es gibt diese Seite auch in einer kreativen Version.": "This page also comes in a creative version.", "Dort gibt es Bewegung und Zeichnungen.": "It has movement and drawings.",
 "Der Inhalt ist der gleiche.": "The content is the same.", "Zur kreativen Version wechseln": "Switch to the creative version", "Nach oben": "Back to top",
 "Rechtliches": "Legal", "Hier finden Sie das Impressum und die Datenschutz-Erklärung.": "Here you find the legal notice and the privacy notice.", "Diese zwei Seiten sind nicht in Leichter Sprache.": "These two pages are in German and not in easy English.",
}

def translate_block(block):
    missing = []
    def tx1(t):
        key = t.strip()
        if not key or not re.search(r'[A-Za-zÄÖÜäöüß]', key): return t
        if key in T: return t.replace(key, T[key])
        missing.append(key); return t
    def tx(t):
        # Text kann geschützte SVG-Marken enthalten: Teile einzeln übersetzen
        return ''.join(part if part.startswith('\x00') else tx1(part) for part in re.split(r'(\x00SVG\d+\x00)', t))
    # SVGs schützen
    svgs = []
    def keep(m): svgs.append(m.group(0)); return '\x00SVG%d\x00' % (len(svgs) - 1)
    out = re.sub(r'<svg.*?</svg>', keep, block, flags=re.S)
    out = re.sub(r'>([^<>]+)<', lambda m: '>' + tx(m.group(1)) + '<', out)
    out = re.sub(r'((?:aria-label|title|alt)=")([^"]+)(")', lambda m: m.group(1) + tx(m.group(2)) + m.group(3), out)
    out = re.sub(r'\x00SVG(\d+)\x00', lambda m: svgs[int(m.group(1))], out)
    # IDs, Anker und Zuordnungen mit en- Präfix (deutsche Sonderseiten bleiben)
    keep_ids = {'freigabe', 'impressum', 'datenschutz'}
    out = re.sub(r'\bid="([^"]+)"', lambda m: 'id="en-%s"' % m.group(1), out)
    out = re.sub(r'\b(aria-labelledby|for|data-act)="([^"]+)"', lambda m: '%s="en-%s"' % (m.group(1), m.group(2)), out)
    out = re.sub(r'href="#([^"]+)"', lambda m: 'href="#%s"' % (m.group(1) if m.group(1) in keep_ids else 'en-' + m.group(1)), out)
    return out, missing

src_path = sys.argv[1]
s = open(src_path, encoding='utf-8').read()
def block(start, end):
    a = s.index(start); b = s.index(end, a); return s[a:b]
kre = block('<div id="kreativ">', '\n<div class="leicht" id="leicht" hidden>')
lei = block('<div class="leicht" id="leicht" hidden>', '\n<!-- EN:START' if '<!-- EN:START' in s else '\n<div class="freigabe" id="freigabe" hidden>')
en_k, m1 = translate_block(kre)
en_l, m2 = translate_block(lei)
en_k = en_k.replace('<div id="en-kreativ">', '<div id="en" lang="en" hidden>', 1)
en_l = en_l.replace('<div class="leicht" id="en-leicht" hidden>', '<div class="leicht" id="en-leicht" lang="en" hidden>', 1)
# Kennzeichnungen im englischen Block aus der deutschen Übersicht heraushalten: data-note beibehalten, aber data-chk-en markieren
en_block = '\n<!-- EN:START (automatisch erzeugt aus den deutschen Blöcken, bitte nicht von Hand bearbeiten) -->\n' + en_k + '\n' + en_l + '\n<!-- EN:END -->\n'
if '<!-- EN:START' in s:
    a = s.index('\n<!-- EN:START'); b = s.index('<!-- EN:END -->') + len('<!-- EN:END -->\n')
    s = s[:a] + en_block + s[b:]
else:
    marker = '\n<div class="freigabe" id="freigabe" hidden>'
    s = s.replace(marker, en_block + marker, 1)
open(src_path, 'w', encoding='utf-8').write(s)
missing = sorted(set(m1 + m2))
print('EN-Blöcke erzeugt. Unübersetzt:', len(missing))
for m in missing: print('  FEHLT:', repr(m))
