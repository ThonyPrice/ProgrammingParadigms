-- Programmeringparadigm HT2016   - F2
-- Ousainou Manneh & Thony Price  - Cdate2

module F2 where
import Data.List 

-- 2.   Molekylära sekvenser
-- 2.1  Skapa datatypen MolSeq för molekylära sekvenser som anger
--      sekvensnamn, sekvens(ensträng), och om det är DNA eller
--      protein som sekvensen beskriver

data MolSeq = DNA [Char] [Char] | Protein [Char] [Char] deriving (Eq, Ord, Read, Show)
data SType = SDNA | SProtein deriving (Eq, Ord, Read, Show)

seqType::MolSeq->SType
seqType (DNA _ _) = SDNA
seqType (Protein _ _) = SProtein

-- 2.2  Skriv en funktion string2seq med typsignaturen
--      String -> String -> MolSeq.Dess första argument är ett namn och
--      andra argument är en sekvens. Denna funktion ska automatiskt skilja
--      på DNA och protein, genom att kontrollera om en sekvens bara
--      innehåller A, C, G, samt T och då utgå ifrån att det är DNA.

string2seq :: String -> String -> MolSeq
-- Första argumentet är ett namn, andra är en sekvens
string2seq n sekvens
  | length sekvens > length x = Protein n sekvens
  | otherwise = DNA n sekvens   
  where x = [x | x <- sekvens, x `elem` "AGCT"]

-- 2.3  Skriv tre funktioner seqName, seqSequence, seqLength som tar en
--      MolSeq och returnerar namn, sekvens, respektive sekvenslängd. Du ska
--      inte behöva duplicera din kod beroende på om det är DNA eller protein!

-- Skapa MolSeq objekt att testa funktionerna under med
create = string2seq "namnet-DNA" "GAGCTTTT"
create2 = string2seq "namnet-DNA2" "GAGCGGGG"

-- Egentligen ska det finnas ett sätt att göra detta utan kodrepetering,
-- gäller även funktionerna seqSequence och seqLength också
seqName :: MolSeq -> String
-- Retunerar namnet 
seqName (DNA n _ ) = n
seqName (Protein n _ ) = n

seqSequence :: MolSeq -> [Char]
-- Retunerar sekvensen
seqSequence (DNA _ s ) = s
seqSequence (Protein _ s ) = s

seqLength :: MolSeq -> Int
-- Retunerar sekvensens längd. OBS! Kan snabbas upp, length = långsam
seqLength (DNA _ s ) = length s
seqLength (Protein _ s ) = length s

-- 2.4  Implementera seqDistance :: MolSeq -> MolSeq -> Double som jämför två 
--      DNA-sekvenser eller två proteinsekvenser och returnerar deras evolutionära avstånd.
--      Om man försöker jämföra DNA med protein ska det signaleras ett fel med hjälp av 
--      funktionen error. Du kan anta att de två sekvenserna har samma längd, 
--      och behöver inte hantera fallet att de har olika längd.

seqDistance :: MolSeq -> MolSeq -> Double
seqDistance x@(DNA _ _) y@(DNA _ _)
  | (1-alfa) > 0.74 = 3.3 
  | otherwise = (-0.75)*log(1.0-((4.0*(1-alfa))/3.0)) 
  where alfa = hamming (seqSequence x) (seqSequence y) (seqLength y)
seqDistance x@(Protein _ _) y@(Protein _ _)
  | (1-alfaP) >= 0.94 = 3.7 
  | otherwise = (-0.95)*log(1-((20*(1-alfaP))/19)) 
  where alfaP = hamming (seqSequence x) (seqSequence y) (seqLength y)
seqDistance (DNA _ _) (Protein _ _) = error "Fel..."
seqDistance (Protein _ _) (DNA _ _) = error "Fel..."

hamming :: [Char] -> [Char] -> Int -> Double
-- När båda sekvenserna är jämförda, retunera täljare över nämnare
hamming [] [] n = 0.0
hamming _ _ 0 = 0.0
hamming (x:xs) (y:ys) n
  | x == y = (fromIntegral(1) / fromIntegral(n)) + hamming xs ys n
  | otherwise = hamming xs ys n

-- 3.   Profiler och sekvenser
-- 3.1  Skapa en datatyp Profile för att lagra profiler. Datatypen ska lagra 
--      information om den profil som lagras med hjälp av matrisen M (enligt 
--      beskrivningen ovan), det är en profil för DNA eller protein, hur många 
--      sekvenser profilen är byggd ifrån, och ett namn på profilen.

data Profile = Profile [[(Char,Double)]] SType Int String deriving (Eq, Ord, Read, Show)

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
    t = seqType (head sl)
    defaults = 
      if (t == SDNA) then
        zip nucleotides (replicate (length nucleotides) 0) -- Rad (i)
      else 
        zip aminoacids (replicate (length aminoacids) 0)   -- Rad (ii)
    strs = map seqSequence sl                              -- Rad (iii)
    tmp1 = map (map (\x -> ((head x), ((fromIntegral(length x)/fromIntegral(length(sl)))))) . group . sort)
               (transpose strs)                            -- Rad (iv)
    equalFst a b = (fst a) == (fst b)
    res = map sort (map (\l -> unionBy equalFst l defaults) tmp1)

molseqs2profile::String->[MolSeq]->Profile
molseqs2profile n m = (Profile (makeProfileMatrix m) (seqType(m!!0)) (length m) (n))  

-- 2.3  Skriv en funktion profileName :: Profile -> String som returnerar en profils
--      namn, och en funktion profileFrequency :: Profile -> Int -> Char -> Double 
--      som tar en profil p, en heltalsposition i, och ett tecken c, och returnerar 
--      den relativa frekvensen för tec- ken c på position i i profilen p (med andra ord, 
--      värdet på elementet mc,i i profilens matris M ).

profileName::Profile -> String
profileName (Profile _ _ _ s) = s

profileFrequency::Profile -> Int -> Char -> Double
profileFrequency (Profile m t r _) i c 
  | t == SDNA = snd((m!!i)!!pos_D c nucleotides 0)
  | otherwise = snd((m!!i)!!pos_P c aminoacids 0)

pos_P::Char->String->Int->Int
pos_P c (x:xs) index
  | c == x = index
  | otherwise = pos_P c xs (index+1)

pos_D::Char->String->Int->Int
pos_D c (x:xs) index
  | c == x = index
  | otherwise = pos_D c xs (index+1)
  
-- Egenkonstruerade testfall

a = string2seq "A" "ACATAA"
b = string2seq "B" "AAGTCA"
c = string2seq "C" "ACGTGC"
d = string2seq "D" "AAGTTC"
e = string2seq "E" "ACGTAA"
f = [a,b,c,d,e]
g = makeProfileMatrix f
h = Profile g SDNA 8 "Name-test"

-- 3.4  Skriv profileDistance :: Profile -> Profile -> Double. Avståndet mellan två 
--      profiler M och M′ mäts med hjälp av funktionen d(M,M′) beskriven ovan.

profileDistance::Profile->Profile->Double
profileDistance (Profile (p:ps) _ _ _) (Profile (q:qs) _ _ _) = sumDist (p:ps) (q:qs)

sumDist::[[(Char,Double)]]->[[(Char,Double)]]->Double
sumDist [] _ = 0.0
sumDist (p:ps) (q:qs)
  | length (p:ps) > 0 = sumRow p q + sumDist ps qs
  | otherwise = 0.0

sumRow::[(Char,Double)]->[(Char,Double)]->Double
sumRow [] _ = 0.0
sumRow (p:ps) (q:qs)
  | length (p:ps) > 0 = abs(snd(p)-snd(q)) + sumRow ps qs
  | otherwise = 0.0
  
-- sumRow::[[(Char,Double)]]->[[(Char,Double)]]->Double
-- sumRow [] [] = 0.0
-- sumRow (p:ps) (q:qs) = (map (getCol p) [0.0..realToFrac(length(p!!0)-1)])
-- -- sumRow (p:ps) (q:qs) = map abs (zipWith (-) (map (getCol p) [0..(length(p!!0)-1)]) (map (getCol q) [0..(length(q!!0)-1)])) + sumRow ps qs 
-- 
-- getCol::[(Char,Double)]->Int->Double
-- getCol p i = snd((p!!0)!!i)

-- sumProfile::[[(Char,Double)]]->Int->Double 
-- sumProfile m it
--   | it == 4 = 0.0
--   | otherwise = sum ( map (getRow m it) [0..(length m - 1)] ) + sumProfile m (it+1)
--   where getRow p i j = snd((p!!j)!!i)
  
-- 4.   Generell beräkning av avståndsmatriser
-- 4.1  Implementera typklassen Evol och låt MolSeq och Profile bli instanser av 
--      Evol. Alla instanser av Evol ska implementera en funktion distance som mäter 
--      avstånd mellan två Evol, och en funktion name som ger namnet på en Evol. Finns 
--      det någon mer funktion som man bör implementera i Evol?

class Evol a where
  name :: a -> String
  distance:: a -> a -> Double
  distanceMatrix::[a] -> [(String, String, Double)]
  
instance Evol MolSeq where
  name a = seqName a 
  distance a b = seqDistance a b
  distanceMatrix a = dMatrix a 
  
instance Evol Profile where
  name a = profileName a 
  distance a b = profileDistance a b
  distanceMatrix a = dMatrix a

dMatrix::Evol a =>[a]->[(String, String, Double)]
dMatrix [] = []
dMatrix (a:as) = helps a (a:as) ++ distanceMatrix(as)

helps::Evol a =>a->[a]->[(String, String, Double)]
helps a [] = []
helps a (b:bs) = (name a, name b, distance a b) : helps a bs

-- getNames::[a]->String
-- getNames [a] = map helps [0..length([a]-1)]
--   where helps i = name(i)