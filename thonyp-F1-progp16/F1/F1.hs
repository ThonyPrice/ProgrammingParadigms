-- ProgP16 - Lab F1 - Uppvarmning i Haskell
-- Ousainou Manneh & Thony Price - CDATE

module F1 where
import Data.Char
-- Importera nödvändiga moduler för uppgiften

-- Del 1/4 Fibonacci

fib :: Integer -> Integer
-- Kräver två basfall för att stoppa rekursionen. 
fib 0 = 0
fib 1 = 1
-- Räknar genom rekursion ut fibionaccitalet n
fib n = fib(n-1) + fib(n-2) 

-- Del 2/4 Rovarspraket

vokaler = ["a", "e", "i", "o", "u", "y"]
-- Lista med vokaler att stämma av mot i rovarsprak och karpsravor

rovarsprak::[Char]->[Char]
-- Basfall om listan är tom
rovarsprak [] = []
-- Om head av [Char] är vokal, ej "o", gå vidare
-- Om head av [Char] är en konsonant, appenda o och upprepa
rovarsprak (a:as)
  |[a] `elem` vokaler = [a] ++ rovarsprak as
  |otherwise = [a] ++ "o" ++ [a] ++ rovarsprak as 

karpsravor::[Char]->[Char]
-- Eftersom vi vet säkert att funktionen avkodar korrekt rovarsprak
-- vet vi att vid varje konsonant kan vi kasta bort följande element "o"
karpsravor [] = []
karpsravor (a:as)
  |[a] `elem` vokaler = [a] ++ karpsravor as
  |otherwise = [a] ++ karpsravor (drop 2 as)

-- Del 3/4 Medellangd

medellangd:: [Char]-> Double
-- Basfall för tom lista
medellangd [] = 0
-- konvertera  parantesen från bokstäver till ord (fromIntegral)
-- Täljaren i parantesen tar längden av en lista med alla bookstäver i strängen
-- Nämnaren i parantesen tar längden av lista med antalet ord i strängen
medellangd a = fromIntegral(length ([n | n<-a, isAlpha n == True])) / fromIntegral(length (helplangd a []))

helplangd :: String -> String -> [String]
-- Basfall för att stoppa iterationen om båda variabler är tomma eller första är tom
helplangd "" ""  = []
helplangd "" add = [add]
-- Strängen delas upp i head och tail
helplangd (a:as) ""
-- Är head en bokstav adderas den till andra variablen och helplangd itereras om på tail
    |isAlpha a = helplangd as [a]
    |otherwise = helplangd as ""
helplangd (a:as) add
    |isAlpha a = helplangd as (a:add)
    |otherwise = add : helplangd as ""

-- Del 4/4 Listskyffling

skyffla:: [x] -> [x]
-- Basfall då listan är tom
skyffla [] = []
-- Är längden av listan x så retuneras x
-- Annars skickas listan till helps tillsammans med index och dess längd
skyffla x
    |length x == 1 = x
    |otherwise = helps x 0 ((length x) -1) ++ skyffla ((helps x 1 ((length x) -1)))

helps:: [x]-> Int -> Int -> [x]
-- Basfall om listan endast innehåller ett element
helps [] _ _ = []
-- Så länge index finns i listan tas det indexerade elementet ut, index 
-- uppdateras och skickas till help igen
helps x index max
    |index <= max =    x!!index :helps x (index+2) max
    |otherwise = []


