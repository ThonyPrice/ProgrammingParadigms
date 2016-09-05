-- ProgP16 - Lab F1 - Uppvarmning i Haskell
-- Ousainou Manneh & Thony Price - CDATE

module F1 where
import Data.Char

-- Del 1/4 Fibonacci

fib :: Integer -> Integer
-- Kräver två basfall för att stoppa rekursionen. 
fib 0 = 0
fib 1 = 1
fib n = fib(n-1) + fib(n-2) 

-- Del 2/4 Rovarspraket

vokaler = ["a", "e", "i", "o", "u", "y"]
-- Lista med vokaler att stämma av mot i rovarsprak och karpsravor

rovarsprak::[Char]->[Char]
-- Om head av [Char] är vokal, ej "o", gå vidare
-- Om head av [Char] är en konsonant, appenda o och upprepa
rovarsprak [] = []
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
-- Utför divisionen som av antal bokstaver och antal ord
medellangd [] = 0
medellangd a = fromIntegral(length ([n | n<-a, isAlpha n == True])) / fromIntegral(length (helplangd a []))

helplangd :: String -> String -> [String]
-- Hjalper medellangd att rakna antal bokstaver/ord
helplangd "" ""  = []
helplangd "" add = [add]
helplangd (a:as) ""
    |isAlpha a = helplangd as [a]
    |otherwise = helplangd as ""
helplangd (a:as) add
    |isAlpha a = helplangd as (a:add)
    |otherwise = add : helplangd as ""

-- Del 4/4 Listskyffling

skyffla:: [x] -> [x]
-- Kontrollerar om listan ar tom annars skickar till helps
skyffla [] = []
skyffla x
    |length x == 1 = x
    |otherwise = helps x 0 ((length x) -1) ++ skyffla ((helps x 1 ((length x) -1)))

helps:: [x]-> Int -> Int -> [x]
-- Hjalper skyffla att flytta index till ratt position
helps [] _ _ = []
helps x index max
    |index <= max =    x!!index :helps x (index+2) max
    |otherwise = []
