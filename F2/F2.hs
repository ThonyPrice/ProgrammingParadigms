-- Programmeringparadigm HT2016   - F2
-- Ousainou Manneh & Thony Price  - Cdate2

module F2 where
import Data.List 

-- 2.   Molekylära sekvenser
-- 2.1  Skapa datatypen MolSeq för molekylära sekvenser som anger
--      sekvensnamn, sekvens(ensträng), och om det är DNA eller
--      protein som sekvensen beskriver

data Molseq = DNA [Char] [Char] | Protein [Char] [Char] deriving (Eq, Ord, Read, Show)
data SType = SDNA | SProtein deriving (Eq, Ord, Read, Show)

seqType::Molseq->SType
seqType (DNA _ _) = SDNA
seqType (Protein _ _) = SProtein

-- 2.2  Skriv en funktion string2seq med typsignaturen
--      String -> String -> MolSeq.Dess första argument är ett namn och
--      andra argument är en sekvens. Denna funktion ska automatiskt skilja
--      på DNA och protein, genom att kontrollera om en sekvens bara
--      innehåller A, C, G, samt T och då utgå ifrån att det är DNA.

string2seq :: String -> String -> Molseq
-- Första argumentet är ett namn, andra är en sekvens
string2seq n sekvens
  | length sekvens > length x = Protein n sekvens
  | otherwise = DNA n sekvens   
  where x = [x | x <- sekvens, x `elem` "AGCT"]

-- 2.3  Skriv tre funktioner seqName, seqSequence, seqLength som tar en
--      MolSeq och returnerar namn, sekvens, respektive sekvenslängd. Du ska
--      inte behöva duplicera din kod beroende på om det är DNA eller protein!

-- Skapa Molseq objekt att testa funktionerna under med
create = string2seq "namnet-DNA" "GAGCTTTT"
create2 = string2seq "namnet-DNA2" "GAGCGGGG"

-- Egentligen ska det finnas ett sätt att göra detta utan kodrepetering,
-- gäller även funktionerna seqSequence och seqLength också
seqName :: Molseq -> String
-- Retunerar namnet 
seqName (DNA n _ ) = n
seqName (Protein n _ ) = n

seqSequence :: Molseq -> [Char]
-- Retunerar sekvensen
seqSequence (DNA _ s ) = s
seqSequence (Protein _ s ) = s

seqLength :: Molseq -> Int
-- Retunerar sekvensens längd. OBS! Kan snabbas upp, length = långsam
seqLength (DNA _ s ) = length s
seqLength (Protein _ s ) = length s

-- 2.4  Implementera seqDistance :: MolSeq -> MolSeq -> Double som jämför två 
--      DNA-sekvenser eller två proteinsekvenser och returnerar deras evolutionära avstånd.
--      Om man försöker jämföra DNA med protein ska det signaleras ett fel med hjälp av 
--      funktionen error. Du kan anta att de två sekvenserna har samma längd, 
--      och behöver inte hantera fallet att de har olika längd.

seqDistance :: Molseq -> Molseq -> Double
seqDistance x@(DNA _ _) y@(DNA _ _)
  | alfa > 0.74 = 3.3 
  | otherwise = (-0.75)*log(1-((4*alfa)/3)) 
  where alfa = hamming (seqSequence x) (seqSequence y) (seqLength y)
seqDistance x@(Protein _ _) y@(Protein _ _)
  | alfaP >= 0.94 = 3.7 
  | otherwise = (-0.95)*log(1-((20*alfaP)/19)) 
  where alfaP = hamming (seqSequence x) (seqSequence y) (seqLength y)
seqDistance (DNA _ _) (Protein _ _) = 0.0
seqDistance (Protein _ _) (DNA _ _) = 0.0

hamming :: [Char] -> [Char] -> Int -> Double
-- När båda sekvenserna är jämförda, retunera täljare över nämnare
hamming [] [] n = 0.0
hamming (x:xs) (y:ys) n
  | x == y = fromIntegral(1) / fromIntegral(n) + hamming xs ys n
  | otherwise = hamming xs ys n

-- 3.   Profiler och sekvenser
-- 3.1  Skapa en datatyp Profile för att lagra profiler. Datatypen ska lagra 
--      information om den profil som lagras med hjälp av matrisen M (enligt 
--      beskrivningen ovan), det är en profil för DNA eller protein, hur många 
--      sekvenser profilen är byggd ifrån, och ett namn på profilen.

nucleotides = "ACGT"
aminoacids = sort "ARNDCEQGHILKMFPSTWYVX"

makeProfileMatrix :: [Molseq] -> [[(Char,Double)]]
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
    tmp1 = map (map (\x -> ((head x), fromIntegral(length x))) . group . sort)
               (transpose strs)                            -- Rad (iv)
    equalFst a b = (fst a) == (fst b)
    res = map sort (map (\l -> unionBy equalFst l defaults) tmp1)

-- 3.2  Skriv en funktion molseqs2profile :: String -> [MolSeq] -> Profile som 
--      returnerar en profil från de givna sekvenserna med den givna strängen som 
--      namn. Som hjälp för att skapa profil-matrisen har du koden i figur 2. 
--      Vid redovisning ska du kunna förklara exakt hur den fungerar, speciellt 
--      raderna (i)-(iv). Skriv gärna kommentarer direkt in i koden inför redovisningen, 
--      för så här kryptiskt ska det ju inte se ut!

-- 2.3  Skriv en funktion profileName :: Profile -> String som returnerar en profils
--      namn, och en funktion profileFrequency :: Profile -> Int -> Char -> Double 
--      som tar en profil p, en heltalsposition i, och ett tecken c, och returnerar 
--      den relativa frekvensen för tec- ken c på position i i profilen p (med andra ord, 
--      värdet på elementet mc,i i profilens matris M ).

-- 3.4  Skriv profileDistance :: Profile -> Profile -> Double. Avståndet mellan två 
--      profiler M och M′ mäts med hjälp av funktionen d(M,M′) beskriven ovan.