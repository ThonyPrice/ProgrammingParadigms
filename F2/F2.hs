-- Programmeringparadigm HT2016   - F2
-- Ousainou Manneh & Thony Price  - Cdate2

module F2 where
import Data.List 

-- 2.   Molekylära sekvenser
-- 2.1  Skapa datatypen MolSeq 

-- Datatypen MolSeq har antingen typen DNA eller Protein,
-- båda två tar två parametrar, namn och sekvens.
data MolSeq = DNA [Char] [Char] | Protein [Char] [Char] deriving (Eq, Ord, Read, Show)
data SType = SDNA | SProtein deriving (Eq, Ord, Read, Show)

-- 2.2  Skriv en funktion string2seq som retuerar samt skiljer på DNA och Protein

-- Enligt datatyp krävs två strängar, namn och sekvens för att skapa Molseq
string2seq :: String -> String -> MolSeq
string2seq n sekvens
-- Om sekvensen blir blir kortare med listvillkor x där endast bokstäver tillhörande
-- DNA-sekvenser tas ut vet vi säkert att det är en Proteinsekvens.
  | length sekvens > length x = Protein n sekvens
  | otherwise = DNA n sekvens   
  where x = [x | x <- sekvens, x `elem` "AGCT"]

-- 2.3  Skriv MolSeq-funktioner som returnerar namn, sekvens, respektive sekvenslängd.

-- Ta en MolSeq och retunera endast första parametern (strängen)
seqName :: MolSeq -> String
seqName (DNA n _ ) = n
seqName (Protein n _ ) = n

-- Ta en MolSeq och retunera endast andra parametern (sekvensen)
seqSequence :: MolSeq -> [Char]
seqSequence (DNA _ s ) = s
seqSequence (Protein _ s ) = s

-- Ta en MolSeq och retunera endast andra parametern (sekvensen)
seqLength :: MolSeq -> Int
seqLength (DNA _ s ) = length s
seqLength (Protein _ s ) = length s

-- 2.4  Implementera seqDistance :: MolSeq -> MolSeq -> Double som jämför två 
--      DNA-sekvenser eller två proteinsekvenser och returnerar deras evolutionära avstånd.

-- Möntermatchning tar alla kombinationer av DNA och MolSeq och retunerar error om ej samma 
seqDistance :: MolSeq -> MolSeq -> Double
seqDistance x@(DNA _ _) y@(DNA _ _)
-- Villkor för alfa och ekvationer tagna ur labbinstruktioner. Notera att alfa 
-- formellt beskriver hur olika sekvenserna är _men_ vi kollar hur lika sekvenserna
-- är därför krävs (1-alfa)
  | (1-alfa) > 0.74 = 3.3 
  | otherwise = (-0.75)*log(1.0-((4.0*(1-alfa))/3.0)) 
  where alfa = hamming (seqSequence x) (seqSequence y) (seqLength y)
seqDistance x@(Protein _ _) y@(Protein _ _)
  | (1-alfaP) >= 0.94 = 3.7 
  | otherwise = (-0.95)*log(1-((20*(1-alfaP))/19)) 
  where alfaP = hamming (seqSequence x) (seqSequence y) (seqLength y)
seqDistance (DNA _ _) (Protein _ _) = error "Fel..."
seqDistance (Protein _ _) (DNA _ _) = error "Fel..."

-- Hjälpfunktion för seqDistance. Tar två sekvenser, dess längd och kollar hur lika de är.
hamming :: [Char] -> [Char] -> Int -> Double
hamming [] [] n = 0.0
hamming (x:xs) (y:ys) n
-- Är bokstäverna lika, addera 1 över längden rekursivt till basfall (tom lista) är nått
  | x == y = (fromIntegral(1) / fromIntegral(n)) + hamming xs ys n
  | otherwise = hamming xs ys n

-- 3.   Profiler och sekvenser
-- 3.1  Skapa en datatyp Profile. Datatypen ska lagra information om den profil som lagras 
--      med hjälp av matrisen M, profil för DNA/protein, hur många sekvenser och ett namn

data Profile = Profile [[(Char,Double)]] SType Int String deriving (Eq, Ord, Read, Show)

-- Ta en Molseq och ange om det är ett DNA eller Protein
-- Eftersom namnen DNA och Protein är tagna används S-prefixet
seqType::MolSeq->SType
seqType (DNA _ _) = SDNA
seqType (Protein _ _) = SProtein

-- 3.2  Skriv en funktion MolSeqs2profile :: String -> [MolSeq] -> Profile som 
--      returnerar en profil från de givna sekvenserna med den givna strängen som 
--      namn. Som hjälp för att skapa profil-matrisen har du koden i figur 2. 
--      Vid redovisning ska du kunna förklara exakt hur den fungerar, speciellt 
--      raderna (i)-(iv). Skriv gärna kommentarer direkt in i koden inför redovisningen, 
--      för så här kryptiskt ska det ju inte se ut!

nucleotides = "ACGT"
aminoacids = sort "ARNDCEQGHILKMFPSTWYVX"

makeProfileMatrix :: [MolSeq] -> [[(Char,Double)]]
makeProfileMatrix [] = error "Empty sequence list"
makeProfileMatrix sl = res
  where 
    -- head sl ger första MolSeq i listan av MolSeq's
    t = seqType (head sl)
    defaults = 
      if (t == SDNA) then
      -- Om typen är (S)DNA gör en lista med tupler i vilken det första elementet är
      -- en första bokstaven från nucleotides och andra elementet noll. Andra tuplen
      -- andra bokstaven och 0 osv.
        zip nucleotides (replicate (length nucleotides) 0) -- Rad (i)
      else 
      -- Samma som kommentar ovan men (S)DNA -> (S)Protein och nucleotides -> aminoacids
        zip aminoacids (replicate (length aminoacids) 0)   -- Rad (ii)
    -- Gör seqSequence (retunera sekvensen) för all MolSeq's i listan
    strs = map seqSequence sl                              -- Rad (iii)
    -- Inne:  lambdafunktionen retunerar en tupel där första elementet är head av inparametern x,
    --        Andra elementet i tupeln, x, sorteras först (i bokstavsordning), sedan grupperas det och sist 
    --        tas längden av x/antal rader i matrisen dvs. length (sl)
    -- 
    -- Ute:   Denna funktion uförs sedan på alla element i transpose ->
    -- (Transpose strs) transponerar strs så alla första elementen är i en lista alla andra i nästa osv.
    tmp1 = map (map (\x -> ((head x), (fromIntegral(length x)/fromIntegral(length(sl))))) . group . sort)
               (transpose strs)                            -- Rad (iv)
    equalFst a b = (fst a) == (fst b)
    res = map sort (map (\l -> unionBy equalFst l defaults) tmp1)

-- Tar namn och en lista MolSeq's och retunerar en Profil med matrisen fr.makeProfileMatrix,
-- typen, längden (antalet rader i matrisen) och namnet.
molseqs2profile::String->[MolSeq]->Profile
molseqs2profile n m = (Profile (makeProfileMatrix m) (seqType(m!!0)) (length m) (n))  

-- 2.3  Skriv en funktion profileName som returnerar en profils namn, och en funktion 
--      profileFrequency som tar en profil p, en heltalsposition i, och ett tecken c, och returnerar 
--      den relativa frekvensen för tecknet c på position i i profilen p.

-- Retunera endast strängen (namnet) från en profil
profileName::Profile -> String
profileName (Profile _ _ _ s) = s

-- Sök frekvensen för ett tecken c på en heltalsposition i
profileFrequency::Profile -> Int -> Char -> Double
profileFrequency (Profile m typ _ _) i c 
-- Det är givet vilken position, i (kolumn) vill va ta elementet från men vi behöver
-- söka vilken rad det sökta tecknet finns i. Olika hjälpfunktioner för DNA och Protein
  | typ == SDNA = snd((m!!i)!!radDna c nucleotides 0)
  | otherwise = snd((m!!i)!!radProt c aminoacids 0)

-- Tar sekvens från profil, en sträng med "DNA-bokstäver", ett räkneindex. 
-- Itererar till bokstaven är funnen och retunerar index 
radDna::Char->String->Int->Int
radDna c (x:xs) index
  | c == x = index
  | otherwise = radDna c xs (index+1)

-- Samma som för radDna
radProt::Char->String->Int->Int
radProt c (x:xs) index
  | c == x = index
  | otherwise = radProt c xs (index+1)

-- 3.4  Skriv profileDistance :: Profile -> Profile -> Double. Avståndet mellan två 
--      profiler M och M′ mäts med hjälp av funktionen d(M,M′) beskriven i Lab2.

-- Ta ut profilernas "matriser" som är listor av listor och skicka till nestlade 
-- hjälpfunktionerna sumDist och i sin tur sumRow
profileDistance::Profile->Profile->Double
profileDistance (Profile p _ _ _) (Profile q _ _ _) = sumDist p q

sumDist::[[(Char,Double)]]->[[(Char,Double)]]->Double
sumDist [] _ = 0.0
sumDist (p:ps) (q:qs)
-- Så länge det finns listor' i listorna skicka listor' till sumRow och summera dessa
  | length (p:ps) > 0 = sumRow p q + sumDist ps qs
  | otherwise = 0.0

sumRow::[(Char,Double)]->[(Char,Double)]->Double
sumRow [] _ = 0.0
sumRow (p:ps) (q:qs)
-- Medans det finns element i listan beräkna absolutbeloppen av differansen mellan listorna
  | length (p:ps) > 0 = abs(snd(p)-snd(q)) + sumRow ps qs
  | otherwise = 0.0
    
-- 4.   Generell beräkning av avståndsmatriser
-- 4.1  Implementera typklassen Evol och låt MolSeq och Profile bli instanser av 
--      Evol. Alla instanser av Evol ska implementera en funktion distance som mäter 
--      avstånd mellan två Evol, och en funktion name som ger namnet på en Evol. Finns 
--      det någon mer funktion som man bör implementera i Evol?

class Evol a where
-- Här anges metoderna för klassen Evol vilka kan användas av alla Evol's instanser
  name :: a -> String
  distance:: a -> a -> Double
  distanceMatrix::[a] -> [(String, String, Double)]
  
-- Låt MolSeq vara en instans av Evol. Använd tidigare definerade funtioner för att 
-- retunera värden till Evol's metoder
instance Evol MolSeq where
  name a = seqName a 
  distance a b = seqDistance a b
  distanceMatrix a = dMatrix a 
  
instance Evol Profile where
  name a = profileName a 
  distance a b = profileDistance a b
  distanceMatrix a = dMatrix a

-- Ta en lista med Evol's och retunera en lista med tripler (namn, namn avstånd)
dMatrix::Evol a =>[a]->[(String, String, Double)]
dMatrix [] = []
-- Notera att första elementet skickas dubbelt som a (a:as) till hjälpfunktionen help
-- seftersom det ska användas "mot" sig själv. Sen anropas funktionen rekursivt med as.
dMatrix (a:as) = helps a (a:as) ++ dMatrix(as)

-- Skapar tripel av två listor i vilka första elementet är samma.
-- Anropar sedan sig själv genom rekursion och tills alla element är använda 
helps::Evol a =>a->[a]->[(String, String, Double)]
helps a [] = []
helps a (b:bs) = (name a, name b, distance a b) : helps a bs

-- *** Slut *** --

-- Egenkonstruerade testfallsvariabler
a = string2seq "A" "ACATAA"
b = string2seq "B" "AAGTCA"
c = string2seq "C" "ACGTGC"
d = string2seq "D" "AAGTTC"
e = string2seq "E" "ACGTAA"
f = [a,b,c,d,e]
g = makeProfileMatrix f
h = Profile g SDNA 8 "Name-test"