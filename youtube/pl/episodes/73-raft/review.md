# Scenario review

**Verdict:** pass

I read the whole paper (pages 1–18), the whole storyboard and all 52 script segments. I found nothing that blocks recording. Every number checks out against the paper once the Polish number words are read: 2014, NSDI 2012, 150–300 ms, 43, 60, 25.7, 20.8, 4.9, 33/43, 15/43, 14%, 33/41, about 15 ms, more than 10 s, 5 ms, 287 ms, 50 ms, 1000 trials, 513 ms, 12–24 ms and 35 ms. I followed every toy scenario step by step and none breaks a paper rule: the election in term 2, the split vote ending in term 3, commits that only count current-term entries, the consistency check, the nextIndex repair, the election restriction (S5 votes because its log is shorter with the same last term; S2 and S4 refuse because they have a later term), Fig. 8 (a)–(e), and the direct switch from C_old to C_new giving two leaders. Each skeptic question is answered correctly by the next narrator segment. Every refs quote occurs in paper.txt, allowing for line-break hyphenation. The narration is all Polish, with no digits or symbols for the speech synthesizer to misread. The few softer phrasings are simplifications that are true, so I did not put them in must_fix: s017 (the stale leader steps down because the reply carries a higher term, not because of the rejection itself), s023 (when the timeouts are re-randomized), s041 ('nigdy' means 'during the transition'), and s044 (33 of 41 applies to each of the two survey questions separately). The narration leaves out the formal TLA+ specification and safety proof. Neither the abstract, the novel-features list nor the conclusion counts it as a key contribution, so I treated it as an acceptable omission; an optional one-sentence mention would still help.

| Verdict | Claims |
|---|---|
| simplified-ok | 8 |
| supported | 35 |

## Must fix

None.

## Claims

| Segment | Verdict | Claim | Location |
|---|---|---|---|
| s001 | supported | Artykuł Ongaro i Ousterhouta ze Stanfordu, 2014, tytuł 'W poszukiwaniu zrozumiałego algorytmu konsensusu' | p.1 title, footnote |
| s001 | supported | Głównym celem była zrozumiałość | p.3 §4 |
| s002-s003 | supported | Naiwny algorytm: serwer niedostępny podczas commitu zostaje leaderem i nadpisuje zatwierdzony wpis | p.8 §5.4 |
| s005 | simplified-ok | Czekanie na wszystkie serwery: jedna awaria zatrzymałaby system; konsensus ma przetrwać awarie | p.1 §1; p.2 §2 |
| s005 | supported | Każdy log ma te same polecenia w tej samej kolejności | p.2 §2 |
| s006 | supported | Deterministyczne maszyny stanów liczą ten sam stan (x=2, y=1 po x←3, y←1, x←2) | p.2 §2 |
| s006 / storyboard replicated_log | supported | Wystarczy większość; 5 serwerów przeżywa 2 awarie | p.2 §2 |
| s006 | simplified-ok | Chubby i ZooKeeper to przykłady; GFS, HDFS, RAMCloud używają RSM do wyboru leadera i konfiguracji | p.2 §2 |
| s007 | simplified-ok | Paxos Lamporta był standardem; single-decree i multi-Paxos | p.2 §3 |
| s007 | supported | Ankieta na NSDI 2012: mało kto czuje się pewnie, nawet doświadczeni badacze | p.2 §3 |
| s008 | supported | Autorom zajęło to prawie rok, z uproszczonymi objaśnieniami i własnym protokołem | p.2 §3 |
| s008 | supported | Brak powszechnie uzgodnionego multi-Paxos | p.2 §3 |
| s008 / storyboard paxos_problem | supported | Zespół Chubby: ostateczny system będzie oparty na nieudowodnionym protokole | p.3 §3 |
| s009-s010 | supported | Definicje: leader, follower (bierny), candidate, term (numerowany, logiczny zegar), commit (bezpieczny do wykonania) | p.5 §5.1; p.6 Fig. 6 |
| s012 | supported | Raft najpierw wybiera silnego leadera; wpisy płyną tylko od leadera; leader sam decyduje o pozycji wpisu | p.3 §5; p.8 §5.4.1 |
| s013 | supported | Podział na trzy względnie niezależne części; redukcja przestrzeni stanów; log bez dziur | p.3 §4, §5 |
| s014 | supported | Start jako follower; timeout → candidate; większość całego klastra → leader | p.5 §5.2, Fig. 4 |
| s015 | supported | Kolejny timeout zaczyna nowe wybory; candidate/leader z nieaktualnym termem wraca do follower | p.5 §5.1; p.6 §5.2 |
| s016 / storyboard terms | supported | Termy kolejno numerowane, każdy zaczyna się wyborami; przy split vote term kończy się bez leadera | p.5 §5.1, Fig. 5 |
| s017 | simplified-ok | Wymiana termów, aktualizacja do większego; nieaktualny leader dostaje odmowę i wraca do follower | p.5 §5.1; p.4 Fig. 2 |
| s019 | supported | Follower nie wie na pewno, odlicza czas; heartbeaty to puste AppendEntries; timeouty losowe np. 150–300 ms | p.6 §5.2 |
| s020 | supported | Candidate zwiększa term, głosuje na siebie, wysyła RequestVote; 3/5 to większość; jeden głos na term → jeden leader | p.6 §5.2 |
| s022-s023 | simplified-ok | Split vote 2/5 vs 2/5; term bez leadera; losowe timeouty rozstrzygają; bez nich mogłoby się powtarzać w nieskończoność | p.6 §5.2 |
| s025 | supported | Wpis zatwierdzony, gdy leader, który go utworzył, ma go na większości | p.7 §5.3 |
| s026 | supported | Leader ponawia do wolnych followerów; po commicie wykonuje i odpowiada; commitIndex w kolejnych AppendEntries/heartbeatach | p.6-7 §5.3 |
| s027-s028 | supported | AppendEntries niesie index i term poprzedniego wpisu; niezgodność → odmowa; Log Matching | p.7 §5.3; p.5 Fig. 3 |
| s030 | supported | Leader nadpisuje rozbieżne wpisy followera; nextIndex inicjalizowany tuż za końcem logu leadera (tu 3) | p.7 §5.3 |
| s031 | supported | Odmowa → nextIndex−1 i ponowienie; przy zgodności usunięcie konfliktów i dopisanie; leader nigdy nie nadpisuje własnego logu | p.7 §5.3; p.5 Fig. 3 |
| s033-s034 | supported | Election restriction: S1 (ostatni term 1) przegrywa z S2/S4 (term 2); S5 (ten sam term, krótszy) głosuje; dwie większości się przecinają | p.8 §5.4.1 |
| s036-s037 / storyboard fig8_trap | supported | Fig. 8 (a)–(d): wpis z termu 2 na 3/5 nie jest zatwierdzony i S5 może go nadpisać głosami S2, S3, S4 | p.8 Fig. 8 |
| s038-s039 | supported | Fig. 8(e): wpis z bieżącego termu na większości jest zatwierdzony, starsze pośrednio; repliki liczy się tylko dla bieżącego termu | p.8 Fig. 8; p.9 §5.4.2 |
| s040 | supported | Bezpośrednie przełączenie 3→5 może dać dwóch leaderów w jednym termie | p.10 §6, Fig. 10 |
| s041 | simplified-ok | Joint consensus C_old,new: osobne większości obu konfiguracji; potem C_new; klaster obsługuje klientów cały czas | p.10-11 §6 |
| s043 / storyboard user_study | supported | 43 studentów Stanford i Berkeley, dwa wykłady wideo i quizy; na 60 pkt średnio 25,7 vs 20,8; +4,9 | p.13-14 §9.1 |
| s044 | simplified-ok | 33 z 43 lepiej z Rafta; 15 z 43 znało Paxos; wideo Paxos 14% dłuższe; 33 z 41 uznało Raft za łatwiejszy; deklaracje mniej wiarygodne | p.14 §9.1, Fig. 14 |
| s045 / storyboard election_timing | supported | 5 serwerów, broadcast ≈15 ms; bez losowości >10 s przez split votes; 5 ms losowości → mediana 287 ms | p.15 §9.3, Fig. 16 |
| s046 | supported | 50 ms losowości: najgorszy z 1000 prób 513 ms; 12–24 ms: średnio 35 ms | p.15 §9.3 |
| s048 | supported | Niżej leader nie zdąży z heartbeatami → zbędne zmiany leadera, gorsza dostępność; zalecane 150–300 ms | p.15 §9.3 |
| s049 | simplified-ok | Zbyt krótkie timery: follower startuje z wyższym termem, leader ustępuje, zbędne zmiany leadera | p.10 §5.6; p.15 §9.3 |
| s050 | supported | broadcastTime ≪ electionTimeout ≪ MTBF; bezpieczeństwo nie zależy od czasu, dostępność tak; przestój ≈ election timeout | p.10 §5.6 |
| s050 | supported | Wynik równoważny multi-Paxos, równie wydajny; jedna runda od leadera do połowy klastra | p.1 Abstract; p.15 §9.3 |
| s050 / storyboard limitations | supported | Bezliderowy EPaxos ma niższe opóźnienia w WAN, ale kosztem dużej złożoności | p.16 §10 |
| s051 | supported | Podsumowanie: najwyżej jeden leader na term, commit na większości, liczenie tylko bieżącego termu, 33 z 43 | p.5 §5.1; p.9 §5.4.2; p.14 Fig. 14 |

## Coverage

- Raft: algorytm zarządzania replikowanym logiem, wynik równoważny multi-Paxos, równie wydajny: s005, s006, s050
- Zrozumiałość jako główny cel; dekompozycja (leader election, log replication, safety) i redukcja przestrzeni stanów: s001, s008, s013
- Silny leader (wpisy płyną tylko od leadera): s012
- Wybór leadera z losowymi timerami: s019, s020, s022, s023, s045, s046
- Replikacja logu, consistency check, Log Matching, naprawa logu: s025, s026, s027, s028, s030, s031
- Bezpieczeństwo: election restriction i reguła commitu dla poprzednich termów: s033, s034, s036, s037, s038, s039
- Zmiana składu klastra przez joint consensus (nakładające się większości): s040, s041
- Badanie z udziałem użytkowników: 43 studentów, Raft łatwiejszy: s043, s044, s051
- Formalna specyfikacja TLA+ i dowód bezpieczeństwa (§9.2): omitted: Not in the abstract, the novel-features list or the conclusion, so acceptable in a 12-minute video. An optional one-sentence mention would help.
- Log compaction (snapshoty, InstallSnapshot) i interakcja z klientem (linearizability): omitted: Secondary practical extensions, not key contributions in the abstract or conclusion.
- Implementacja (LogCabin, ok. 2000 linii C++, ok. 25 implementacji open source): omitted: Context rather than a contribution; acceptable to leave out.

## Skeptic loop

- ✅ s004 → s005 Waiting for all servers would let one failure block the system; consistent with §2.
- ✅ s011 → s012 Strong leader elected first (§5).
- ✅ s018 → s019 It doesn't know; it assumes no viable leader after the timeout (§5.2).
- ✅ s021 → s022 Split vote, resolved by randomized timeouts in s023.
- ✅ s024 → s025 Commit definition from §5.3; refined later for previous-term entries.
- ✅ s029 → s030 Leader overwrites conflicting follower entries (§5.3).
- ✅ s032 → s033 Overwriting is safe only for uncommitted entries; the election restriction protects committed ones.
- ✅ s035 → s036 Fig. 8 counterexample, followed by the rule in s039.
- ✅ s042 → s043 User study, §9.1.
- ✅ s047 → s048 Violates the timing requirement and causes unnecessary leader changes (§9.3).
