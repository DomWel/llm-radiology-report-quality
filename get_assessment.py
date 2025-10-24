from helper_functions import clean_string
from llm_access_2 import ask_ollama


def staging_assessment(radiology_report, staging_parameter, parameters_dict):
    if staging_parameter == "T":
        # Prompts
        explanation = (
            "Für die folgende Beurteilung ist wichtig, dass bei einem Rektumkarzionm zu unterscheiden ist, "
            "ob dieses auf die Darmwand (also Schleimhaut/Mukosa, Submukosa oder Tunica muscularis) beschränkt ist "
            "oder darüber hinaus wächst."
        )
        command = (
            "Bewerte nun auf einer Skala von 1 bis 10 ob die Informationen im nachfolgenden Befundtext ausreichend "
            "für die Beurteilung der lokalen Ausbreitung sind (T-Status). Beachte: wenn explizit die Infiltration von "
            "Mesorektum bzw. angrenzenden Organen / Strukturen beschrieben ist, so ist von dem Stadium T3 bzw. T4 ausgzugehen, "
            "und die Information ist als ausreichend zu werten. "
            "Wenn das mesorektale Fettgewebe nicht infiltriert wird, gehe davon aus, dass der Tumor auf die Darmwand beschränkt ist "
            "und somit ebenfalls genügend Infos gegeben sind. Kein wandüberschreitendes Wachstum ist ebenfalls als eine suffiziente "
            "Beschreibung zu werten (entsprechend T1/2). "
            "Lymphknoten- und Fernmetastasen sind nicht relevant für diese Fragestellung. "
            "Wenn im Befundtext nur eine spezifische Schicht (z.B. Tunica muscularis) angegeben ist, "
            "dann gehe davon aus, dass dies die maximale Infiltrationstiefe darstellt."
        )
        command_2 = (
            'Extrahiere aus nachfolgendem Text nur die genannte Zahl auf einer Skala von 0 bis 10 und antworte nur '
            'mit der Zahl! Wenn im Text bereits nur eine Zahl enthalten ist (z.B. "1"), dann gebe einfach diese Zahl '
            "wieder!"
        )
        recommendation = (
            "Folgende Situation: das MRT wurde zum Staging beim Rektumkarzinom gemacht. Welche Empfehlung hast du auf Basis "
            "des Befundtextes an den Radiologen, um den Befund zu verbessern sodass das T-Stadium problemlos eingeordnet "
            "werden kann (max. 150 Wörter).         Betone dabei, dass die Infiltrationstiefe in Bezug auf die "
            "Wandschichten des Rektums hochrelevant ist. Inbesondere sollte diskutiert werden, ob die Rektumwand "
            "überschritten wurde         und eine Infiltration des Mesorektums vorherrscht! Gehe bitte nur auf das "
            "T-Stadium ein. Lymphknoten, EMVI und MRF sind bei der Antwort nicht zu berücksichtigen. Zudem gehe nur auf "
            "den Inhalt des Befundes ein, weiterführende Untersuchungen sind nicht relevant!"
        )

        buffer = []
        i = 0  # successful runs
        attempt = 0  # total attempts (optional, for logging)

        while i < parameters_dict["N"]:
            attempt += 1
            try:
                answer = ask_ollama(
                    explanation + "      " + command + "     " + radiology_report,
                    parameters_dict,
                )[1]
                answer = clean_string(str(answer))
                print(answer, flush=True)

                answer_2 = ask_ollama(command_2 + "     " + answer, parameters_dict)[1]
                print(answer_2, flush=True)

                scale_value = int(answer_2)
                buffer.append(scale_value)
                i += 1  # only count successful completions
            except Exception as e:
                print(f"Error on attempt {attempt}: {e}")

        recommendation = 'Deine Antwort: "' + radiology_report + "\n" + recommendation
        answer_recommendation = ask_ollama(recommendation, parameters_dict)[1]
        average = sum(buffer) / len(buffer)

        return average, answer, answer_recommendation

    elif staging_parameter == "EMVI":
        # Prompts
        command_1 = (
            "Bitte analysiere in maximal 150 Wörtern ob in dem Befund darauf eingegangen wird, ob der Tumor "
            "ein perirektales Blutgefäß (insb. Vene) infiltriert. Eine makroskopischee Gefäßinvasionn ist gleichbedeutend "
            "mit einer venösen Geäßinfiltration. Die Negierung eines wandüberschreitenden Wachstums oder einer Infiltration "
            "(ohne Gefäßbezug) schliesst eine Gefäßinfiltration nicht aus. Wir können eine venöse Infiltration nur dann ausschließen, "
            "wenn dies explizit im Text negiert wird oder der  EMVI-Score genannt wird. Bitte verwechsle dies nicht mit Lymphknoten die "
            "entlang einer Vene verteiult sind, das entspricht nicht einer venösen Infiltration!"
        )
        command_2 = (
            "Bewerte nun auf einer Skala von 1 bis 10 (Angabe: P = ...) wie sicher du auf Basis des nachfolgenden Textes bist das "
            "EMVI-Stadium abzuleiten. Bei Nennung von EVMI negativ, EMVI 1 und EMVI 2 ist sicher von keiner Gefäßinfiltration auszugehen (P > 7). "
            "Wenn eine venöse Infiltration weder bestätigt noch negiert wird, ist ein P-Wert <5 zu vergeben! "
            "Wenn eine perirektale Vene/Gefäß signalangehoben oder signalalteriert ist, dann ist dies als starker Hinweis "
            "auf eine Gefäßinfiltration zu werten und ein P-Wert >7 ist zu vergeben!"
        )
        command_3 = (
            "Extrahiere aus dem Text den genannten P-Wert. Bei Intervallen gib nur den unteren Grenzwert zurück. "
            "Das wichtigste ist, dass du nur mit einem einzigen ganzzahligen Wert antwortest! Ansonsten kein Text!"
        )
        recommendation_report = (
            "Bitte erstelle auf Basis des Befundtextes eine Empfehlung (max. 200 Wörter) an mich (ich bin Radiologee), "
            "wie ich den Befund verbessern kann, sodass das EMVI-Stadium daraus entnommen werden kann. "
            "Hier geht es explizit nur um das EMVI-Stadium und ausschließlich um die Verbesserung des Befundtextes "
            "(gehe nicht auf T-/N-Stadium ein und empfehle auch keine weiterführende Diagnostik). "
            "Eine adäquate Beschreibung wäre z.B.: die Erwähnung einer Infiltration/Invasion eines perirektalen Gefäßes mit "
            "Uhrzeitangabe (z. B. auf 9 Uhr) sowie ob das Gefäß signalalteriert und/oder aufgeweitet ist. Falls keine Infiltration vorliegt "
            "ist dies ebenfalls explizit zu erwähnen."
        )

        i = 0  # successful attempts
        attempt = 0  # total attempts (optional, for logging)
        buffer = []

        while i < parameters_dict["N"]:
            attempt += 1
            try:
                answer1 = ask_ollama(
                    command_1 + 'Befundtext: "' + radiology_report + '"', parameters_dict
                )[1]
                print(answer1, flush=True)

                answer2 = clean_string(
                    ask_ollama(
                        command_2 + 'Text: "' + answer1 + '"', parameters_dict
                    )[1]
                )

                try:
                    print(answer2, flush=True)
                    scale_value = int(answer2)
                except:
                    answer3 = ask_ollama(
                        command_3 + "        " + answer2, parameters_dict
                    )[1]
                    print(answer3, flush=True)
                    scale_value = int(answer3)

                buffer.append(scale_value)
                i += 1  # count only successful runs
            except Exception as e:
                print(f"Error on attempt {attempt}: {e}")

        recommendation_prompt = (
            "Befundtext: \n" + radiology_report + "\n" + recommendation_report
        )
        recommendation_report = ask_ollama(
            recommendation_prompt, parameters_dict
        )[1]

        print(buffer)
        average = sum(buffer) / len(buffer)

        return average, answer1, recommendation_report

    elif staging_parameter == "MRF":
        # Prompts
        command_1 = (
            "Bitte analysiere in maximal 150 Wörtern ob in dem Befund darauf eingegangen wird, ob der Tumor die "
            "mesorektale Faszie infiltriert. Wenn der Abstand zur mesorektalen Faszie weniger als 1 mm beträgt ist "
            "ebenfalls von einer Infiltration auszugehen, wenn die minimale Distanz zur MRF > 1 mm misst ist "
            "sie sicher nicht infiltriert. Angaben wie <5 mm sind sehr unsichere Angaben, da letztlich nicht klar "
            "ist ob eine Infiltration stattfindet. Wenn der Tumor die mesorektale Faszie berührt, diese erreicht "
            "oder Kontakt zu ihr hat, ist ebenfalls von einer Infiltration auszugehen. Auch ein möglicher Kontakt "
            "wird als Infiltration gewertet. Ein unmittelbarer Lagebezug ist als uneindeutige Aussage in Bezug auf "
            "die Infiltration zu werten. Wenn der Text den Bezug zur mesorektalen Faszie nicht diskutiert, dann kann "
            "es nicht beurteilt werden und eine hohe Unsicherheit ist anzugeben! Bitte aus der Infiltration des Mesorektum "
            "NICHT ableiten, dass auch die mesorektale Faszie infiltriert sein muss!"
        )
        command_2 = (
            "Bewerte nun auf einer Skala von 1 bis 10 (Angabe: P = ...) wie sicher du auf Basis des nachfolgenden Textes "
            "bist das MRF-Stadium abzuleiten. Wenn du dir sicher bist, dass der Tumor die meosrektale Faszie infiltriert bzw. "
            "nicht infiltriert gebe einen hohen P-Wert aus. Wenn du auf Basis des Textes nicht beurteilen kannst, ob die "
            "mesorektale Faszie infiltriert wird dann gebe einen niedrigen P-Wert aus! Antworte nicht mit \\{ oder \\}!"
        )
        command_3 = (
            'Extrahiere aus dem Text den genannten P-Wert. Bitte verwende nur den Wert der hinter "P = " steht. '
            "Bei Intervallen gib nur den unteren Grenzwert zurück. Das wichtigste ist, dass du nur mit einem einzigen "
            "ganzzahligen Wert antwortest! Wenn nur eine Zahl im Text enthalten ist, dann gebe diese wieder!"
        )
        recommendation_report = (
            "Bitte erstelle mir (ich bin Radiologe) auf Basis des Befundtextes eine Empfehlung (max. 200 Wörter), "
            "wie ich den Befund verbessern kann, sodass das MRF-Stadium daraus sicher entnommen werden kann. "
            "Hier geht es explizit nur um das MEF-Stadium und ausschließlich um die Verbesserung des Befundtextes "
            "(gehe nicht auf T-/N-Stadium ein und empfehle auch keine weiterführende Diagnostik). "
            "Zu einer adäquaten Beschreibung gehört die Angabe des minimalen Abstandes zur mesorektalen Faszie sowie "
            "die zugehörige Lokalisation in Uhrzeitangabe (z.B. 3 Uhr in SSL). Wenn nur ein minimaler Abstand ohne konkrete "
            "Distanzangabe genannt wird, ist dies für den Zuweiser nicht genügend (< 1 mm: MRF+ vs. >1mm: MRF- damit einordenbar). "
            "Falls die mesorektale Faszie nicht infiltriert wird, sollte dies ebenfalls erwähnt werden!"
        )


        buffer = []
        i = 0  # number of successful runs
        attempt = 0  # total attempts (for logging/debugging)

        while i < parameters_dict["N"]:
            attempt += 1
            try:
                answer1 = ask_ollama(
                    command_1 + "        " + radiology_report, parameters_dict
                )[1]
                print(answer1, flush=True)

                answer2 = ask_ollama(
                    command_2 + "        " + answer1, parameters_dict
                )[1]
                print(answer2, flush=True)

                try:
                    scale_value = int(answer2)
                except:
                    answer3 = ask_ollama(
                        command_3 + "        " + str(answer2), parameters_dict
                    )[1]
                    print(answer3, flush=True)
                    scale_value = int(answer3)

                buffer.append(scale_value)
                i += 1  # count successful iteration only
            except Exception:
                print(f"Error on attempt {attempt}. Repeating ...")

        recommendation_prompt = (
            "Befundtext: \n" + radiology_report + "\n" + recommendation_report
        )
        recommendation_report = ask_ollama(
            recommendation_prompt, parameters_dict
        )[1]

        print(buffer)
        average = sum(buffer) / len(buffer)

        return average, answer1, recommendation_report

    elif staging_parameter == "N":
        # Prompts
        command_1 = (
            "Bitte analysiere den nachfolgenden Befundtext in den folgenden Schritten: "
            "Untersuche zunächst ob Lymphknoten im Befund erwähnt werden, wenn nicht kann der Lymphknotenstatus "
            "nicht beurteilt werden. Analysiere dann, ob zu jedem im Befund erwähnten Lymphknoten eine Anzahl "
            "genannt werden kann, wenn ja sind die Informationen ausreichend und du kannst die Untersuchung beenden. "
            "Wenn explizit angegeben ist, dass keine Lymphknoten suspekt sind, ist mit hoher Sicherheit von null suspekten "
            "Lymphknoten auszugehen. Wenn Lymphknoten im unbestimmten Plural angegeben sind, kann die Anzahl "
            "nicht exakt angegeben werden und es folgt Schritt 2. Hier ist es notwendig zu entscheiden, wie hoch die "
            "Wahrscheinlichkeit ist, dass mehr als 3 Lymphknoten suspekt sind. Hierzu addiere die Lymphknoten in "
            "sämtlichen Regionen auf und betrachte die Summe, inkludiere hierbei nur Lymphknoten die auch als "
            "pathologisch oder suspekt gewertet werden. Bei Regionen in den eine unbestimmte Anzahl Lymphknoten angegeben "
            "ist, gehe von mindestens zwei Lymphknoten aus. Bitte antworte nicht nur mit einer Zahl!"
        )
        command_2 = (
            "Bewerte nun auf einer Skala von 1 bis 10 (Angabe: P = ...) wie sicher du auf Basis des nachfolgenden Textes "
            "das N-Stadium beurteilen kannst (entweder keine suspekten Lymphknoten (N0), 1-3 Lymphknoten (N1) oder definitiv "
            "mehr als drei Lymphknoten (N2). Bitte beachte: wenn in zwei verschiedenen Regionen jeweils Lymphknoten im Plural "
            "angegeben werden, dann ist der Lymphknotenstatus sicher als N2 einzuordnen. Wenn mehr als 3 Lymphknotenregionen "
            "genannt werden ist ebenfalls von N2 auszugehen. Wenn du nicht sicher zwischen N1 und N2 unterscheiden kannst, "
            "gib einen niedrigen P-Wert aus!"
        )
        command_3 = (
            "Extrahiere aus dem Text den genannten P-Wert. Bei Intervallen gib nur den unteren Grenzwert zurück. Das wichtigste "
            "ist, dass du nur mit einem einzigen ganzzahligen Wert antwortest! Ansonsten kein Text!"
        )
        recommendation_report = (
            "Bitte erstelle mir (ich bin Radiologe) auf Basis des Befundtextes eine Empfehlung (max. 200 Wörter), "
            "wie ich den Befund verbessern kann, sodass das N-Stadium daraus sicher entnommen werden kann. "
            "Hier geht es explizit nur um das N-Stadium und ausschließlich um die Verbesserung des Befundtextes "
            "(gehe nicht auf das T-Stadium oder EMVI/MRF ein und empfehle auch keine weiterführende Diagnostik). "
            "Für eine Einordnung ist eine exakte Zahlenangabe bei Nennung der suspekten Lymphknoten in einer Region optimal. "
            "Angaben in unbestimmten Plural sind zu vermeiden, da dabei in der Regel nicht zwischen N1 (1-3 path. Lymphknoten) "
            "und N2 (>3 path. Lymphknoten) unterschieden werden kann. Falls dies nicht vermeidbar ist, sollte zumindest "
            "für jede Region explizit eine Mindestanzahl genannt werden."
        )

        buffer = []
        i = 0  # successful runs
        attempt = 0  # total attempts (for logging/debugging)

        while i < parameters_dict["N"]:
            attempt += 1
            try:
                answer1 = ask_ollama(
                    command_1 + '\n Befundtext: "' + radiology_report + '"',
                    parameters_dict,
                )[1]
                answer1 = clean_string(str(answer1))
                print(answer1, flush=True)

                answer2 = ask_ollama(
                    'Antwort: "' + answer1 + '"', parameters_dict
                )[1]
                answer2 = clean_string(str(answer2))
                print(answer2, flush=True)

                try:
                    scale_value = int(answer2)
                except:
                    answer3 = ask_ollama(
                        command_3 + '. "' + answer2 + '"', parameters_dict
                    )[1]
                    print(answer3, flush=True)
                    scale_value = int(answer3)

                buffer.append(scale_value)
                i += 1  # increment only on success
            except Exception as e:
                print(f"Error on attempt {attempt}: {e}")

        recommendation_prompt = (
            "Befundtext: \n" + radiology_report + "\n" + recommendation_report
        )
        recommendation_report = ask_ollama(
            recommendation_prompt, parameters_dict
        )[1]

        print(buffer)
        average = sum(buffer) / len(buffer)

        return average, answer1, recommendation_report

    else:
        print("Please use a valid staging parameter!")