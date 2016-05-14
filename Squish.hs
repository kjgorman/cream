module Squish where

import           Control.Arrow ((&&&), (***))
import           Control.Monad (liftM)
import           Data.List (intercalate)
import           Data.List.Split (splitOn)
import qualified Data.Map as M
import           Data.Time
import           Data.Time.Format
import           System.Locale

between :: UTCTime -> UTCTime -> [Day]
between start end = let startDay = intoDay start
                        endDay   = intoDay end
                        span     = [0..diffDays endDay startDay]
                    in map (flip addDays $ startDay) span

intoDay t = let (y, m, d) = toGregorian $ utctDay t
            in fromGregorian y m d

parseTime :: String -> UTCTime
parseTime = readTime defaultTimeLocale "%e/%m/%Y"

parseTimeseries :: [String] -> [(UTCTime, Float)]
parseTimeseries file = map (parse . extract . splitOn "\t") file :: [(UTCTime, Float)]
    where extract = ((!! 0) &&& (!! 2))
          parse   = (Squish.parseTime *** read)

summarise :: [(UTCTime, Float)] -> [(UTCTime, Float)]
summarise entries = summarise' entries []
    where
      summarise' [] acc = acc
      summarise' (x:xs) [] = summarise' xs [x]
      summarise' ((xd, xb):xs) ((yd, yb):ys) = if (utctDay xd) == (utctDay yd)
                                               then summarise' xs ((xd, xb + yb):ys)
                                               else summarise' xs ((xd, xb):(yd, yb):ys)

toCsvRows :: [(UTCTime, Float)] -> Day -> [String]
toCsvRows entries start = let records = ["Date", "Balance"] : map toRow entries
                              toRow (l, r) = [show (daysDistance l start), show r]
                          in map (intercalate ",") records

daysDistance :: UTCTime -> Day -> Integer
daysDistance date start = diffDays (utctDay date) start

main :: IO ()
main = do
  content <- liftM lines $ readFile "timeseries.csv"
  let headers = head content
      file = tail content

  let running = parseTimeseries file
      opening = head running
      closing = last running
      csvRows = toCsvRows running (utctDay $ fst opening)

  print . show $ length running
  print . show . length $ summarise running
  print $ take 10 csvRows
  writeFile "squished.csv" $ unlines csvRows
