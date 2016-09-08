-- Programmeringparadigm HT2016   - F2
-- Ousainou Manneh & Thony Price  - Cdate2

module F2 where

-- 2.   Molekylära sekvenser
-- 2.1  Skapa datatypen MolSeq för molekylära sekvenser som anger 
--      sekvensnamn, sekvens(ensträng), och om det är DNA eller 
--      protein som sekvensen beskriver

data Molseq = DNA [Char] [Char] | Protein [Char] [Char] deriving (Show)

-- 2.2  Skriv en funktion string2seq med typsignaturen 
--      String -> String -> MolSeq.Dess första argument är ett namn och 
--      andra argument är en sekvens. Denna funktion ska automatiskt skilja 
--      på DNA och protein, genom att kontrollera om en sekvens bara 
--      innehåller A, C, G, samt T och då utgå ifrån att det är DNA.

string2seq :: String -> String -> Molseq
-- Första argumentet är ett namn, andra är en sekvens
string2seq n []   = Protein n []
string2seq n (x:xs)
  | [x] `elem` list = DNA n (x : xs)
  | otherwise = string2seq n xs
  where list = ["A", "C", "G", "T"]

-- ghci klarar av att kompilera koden nu. 
-- Ej testat med hjälpfilen mobio.hs än