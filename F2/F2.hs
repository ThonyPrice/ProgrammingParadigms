-- Programmeringparadigm HT2016   - F2
-- Ousainou Manneh & Thony Price  - Cdate2

module F2 where

-- 2.   Molekylära sekvenser
-- 2.1  Skapa datatypen MolSeq för molekylära sekvenser som anger
--      sekvensnamn, sekvens(ensträng), och om det är DNA eller
--      protein som sekvensen beskriver

data Molseq = DNA [Char] [Char] | Protein [Char] [Char] deriving (Read, Show)

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
create = string2seq "namnet-DNA" "AGGCATCATCGCAT"
create2 = string2seq "namnet-Protein" "AGGCXKKKQATCATCGCAT"

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


