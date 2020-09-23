## Technical Mean Reversion Anomaly

We find some stocks seem reverting around a trend line, although stock price movement is complex. We notice the price of a stock in the short term can deviate from its long-term trend line. The long-term trend can be characterized by a moving average line or a regression. We often find the short-term prices deviate and then reverts back to the regression line. Of various combinations of stock trading strategies, a common type of trading stategies is the mean reversion. It identifies anomalous opportunities as the entry or exit points. This strategy has been quite popular among traders.

- Learning objective 1: Use the R library ["quantmod"](https://cran.r-project.org/web/packages/quantmod/quantmod.pdf), ["TTR"](https://cran.r-project.org/web/packages/TTR/TTR.pdf), and ["PerformanceAnalytics"](https://cran.r-project.org/web/packages/PerformanceAnalytics/PerformanceAnalytics.pdf)
- Learning objective 2: Common stock data transformation
- Learning objective 3: The basic characteristics of stock returns
- Learning objective 4: Common technical indicators
- Learning objective 5: How to plot technical charts
- Learning objective 6: Develop your trading strategy & signals
- Learning objective 7: Backtesting
- Learning objective 8: Use technical indicators as features for machine learning
- Learning objective 9: Python [TA-lib](https://mrjbq7.github.io/ta-lib/). TA-Lib is widely used by trading software developers to perform technical analysis of financial market data.

### Learning objective 1: Use the R library ["quantmod"](https://cran.r-project.org/web/packages/quantmod/quantmod.pdf), ["TTR"](https://cran.r-project.org/web/packages/TTR/TTR.pdf), and ["PerformanceAnalytics"](https://cran.r-project.org/web/packages/PerformanceAnalytics/PerformanceAnalytics.pdf)


```R
#install.packages("PerformanceAnalytics")
```


```R
# The easiest way to get dplyr is to install the whole tidyverse:
library(tidyverse) # https://www.tidyverse.org/
library(dplyr) # or just dplyr
library(quantmod)
library(TTR)
library(PerformanceAnalytics)
library("IRdisplay")
```


```R
getSymbols(c("AMZN","DAL"))
```

    ‘getSymbols’ currently uses auto.assign=TRUE by default, but will
    use auto.assign=FALSE in 0.5-0. You will still be able to use
    ‘loadSymbols’ to automatically load data. getOption("getSymbols.env")
    and getOption("getSymbols.auto.assign") will still be checked for
    alternate defaults.
    
    This message is shown once per session and may be disabled by setting 
    options("getSymbols.warning4.0"=FALSE). See ?getSymbols for details.
    



<ol class=list-inline>
	<li>'AMZN'</li>
	<li>'DAL'</li>
</ol>




```R
df <- AMZN
head(df)
```


               AMZN.Open AMZN.High AMZN.Low AMZN.Close AMZN.Volume AMZN.Adjusted
    2007-01-03     38.68     39.06    38.05      38.70    12405100         38.70
    2007-01-04     38.59     39.14    38.26      38.90     6318400         38.90
    2007-01-05     38.72     38.79    37.60      38.37     6619700         38.37
    2007-01-08     38.22     38.31    37.17      37.50     6783000         37.50
    2007-01-09     37.60     38.06    37.34      37.78     5703000         37.78
    2007-01-10     37.49     37.70    37.07      37.15     6527500         37.15


### Learning objective 2: Common stock data transformation
* These common stock data transformation can be handled easily by the functions in the quantmod library


```R
df2 <- df

# Returns from Open to Close, Hi to Close, or Close to Close 
df2$OpCl <- OpCl(df2)
df2$OpOp <- OpOp(df2) 
df2$HiCl <- HiCl(df2) 
df2$ClCl <- ClCl(df2) 

df2$pcntOpCl1 <- Delt(Op(df2),Cl(df2),k=1)
df2$pcntOpCl2 <- Delt(Op(df2),Cl(df2),k=2)
df2$pcntOpCl3 <- Delt(Op(df2),Cl(df2),k=3)

#One period lag of the close 
df2$lagCl <- Lag(Cl(df2)) 
df2$lag2Cl <- Lag(Cl(df2),2)  
df2$lag3Cl <- Lag(Cl(df2),3) 

# Move up the OpCl by one period
df2$nextOpCl <- Next(OpCl(df2)) 

#head(df2)
```


```R
df.monthly <- to.monthly(df)
df.monthly$month <- format(index(df.monthly),"%Y%m")
df.monthly$year <- format(index(df.monthly),"%Y")
head(df.monthly)
```


             df.Open df.High df.Low df.Close df.Volume df.Adjusted  month year
    Jan 2007   38.68   39.14  36.30    37.67 130435300       37.67 200701 2007
    Feb 2007   37.95   42.00  36.68    39.14 157975400       39.14 200702 2007
    Mar 2007   39.32   40.24  37.04    39.79 142153100       39.79 200703 2007
    Apr 2007   39.85   63.84  39.55    61.33 346287000       61.33 200704 2007
    May 2007   61.12   73.31  59.70    69.14 330242400       69.14 200705 2007
    Jun 2007   68.90   74.72  66.71    68.41 238788700       68.41 200706 2007



```R
rtn.daily <- dailyReturn(df) # returns by day 
rtn.weekly <- weeklyReturn(df) # returns by week 
rtn.monthly <- monthlyReturn(df) # returns by month, indexed by yearmon 
# daily,weekly,monthly,quarterly, and yearly 
rtn.allperiods <- allReturns(df) # note the plural
head(rtn.daily)
```


               daily.returns
    2007-01-03  0.0005170889
    2007-01-04  0.0051679844
    2007-01-05 -0.0136247551
    2007-01-08 -0.0226739386
    2007-01-09  0.0074666400
    2007-01-10 -0.0166754107


### Learning objective 3: The basic characteristics of stock returns
- A standard normal distribution has 0 mean, 1 standard deviation, and 0 excess [kurtosis](http://www.r-tutor.com/elementary-statistics/numerical-measures/kurtosis) 
- The ditribution of a typical stock returns has small standard deviation and positive excess kurtosis


```R
# Generate a standard normal distribution
rn <- rnorm(100000)
print(paste0("standard deviation: ", sd(rn)))
print(paste0("Kurtosis: ", round(kurtosis(rn),2)))
options(repr.plot.width = 4, repr.plot.height = 4)

#hist(rn,breaks=100,prob=TRUE)
#curve(dnorm(x, mean=0, sd=1), col="darkblue", lwd=2, add=TRUE ) # Overlay a standard normal distribution
```

    [1] "standard deviation: 0.998879862990584"
    [1] "Kurtosis: 0.03"



```R
print(paste0("standard deviation: ", sd(rtn.daily)))
print(paste0("Kurtosis: ", round(kurtosis(rtn.daily),2)))

options(repr.plot.width = 4, repr.plot.height = 4)

m<-mean(rtn.daily)
std<-sqrt(var(rtn.daily))
m

# Overlay a standard normal distribution
#curve(dnorm(x, mean=m, sd=std), col="darkblue", lwd=2, add=TRUE )
#hist(rtn.daily, breaks=100, prob=TRUE) # Make it a probability distribution
```

    [1] "standard deviation: 0.024401938344768"
    [1] "Kurtosis: 15.91"



0.00156416346916063



```R
# A really basic boxplot.
df$year <- format(index(df),"%Y")
df$month <- format(index(df),"%Y%m")
df3 <- data.frame(df) %>% filter(year==2014)
df3$AMZN.Volume <- as.numeric(df3$AMZN.Volume)

options(repr.plot.width = 6, repr.plot.height = 3)

# Basic plot
p <-ggplot(df3, aes(x=as.factor(month), y=AMZN.Volume)) 

#p + geom_boxplot(fill="slateblue", alpha=0.2) +  xlab("Month") 
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
# Change outlier, color, shape and size
p2 <- p  + geom_boxplot(outlier.colour="red", outlier.shape=8,
                outlier.size=1) +     xlab("Month")
#p2
```


```R
# Box plot with dot plot
#p2 + geom_dotplot(binaxis='y', stackdir='center', dotsize=0.2, binwidth=40)
```


```R
options(repr.plot.width = 6, repr.plot.height = 4)
df <- AMZN
df$OpCl <- OpCl(df)
df$OpOp <- OpOp(df) 
df$HiCl <- HiCl(df) 
df$month <- format(index(df),"%Y%m")
df$year <- format(index(df),"%Y")
df_hiCl <- df[df$year==2017,]
#boxplot(HiCl~month, data=df_hiCl, notch=TRUE, 
#  col=(c("gold","darkgreen")),
#  main="Hi-Closed", xlab="Month")

#boxplot(OpCl~month, data=df_hiCl, notch=TRUE, 
#  col=(c("gold","darkgreen")),
#  main="Open-Closed", xlab="Month")
```

### Learning objective 4: Common technical indicators

#### MACD
* MACD=12-Period EMA − 26-Period EMA, or "fast EMA - slow FMA"
* The MACD was developed by Gerald Appel and is probably the most popular price oscillator. 
* It can be used as a generic oscillator for any univariate series, not only price.
* The MACD has a positive value whenever the 12-period EMA is above the 26-period EMA and a negative value when the 12-period EMA is below the 26-period EMA. The more distant the MACD is above or below its baseline indicates that the distance between the two EMAs is growing. 

#### RSI
* Introduced by Welles Wilder Jr. in his seminal 1978 book "New Concepts in Technical Trading Systems", the relative strength index (RSI) is a popular momentum indicator.
* It measures the magnitude of recent price changes to evaluate overbought or oversold conditions. 
* The RSI is displayed as an oscillator and can have a reading from 0 to 100.  
* RSI >= 70: a security is overbought or overvalued and may be primed for a trend reversal or corrective pullback in price. 
* RSI <= 30: an oversold or undervalued condition.
* It can be used in the price of a stock or other asset.

#### Bollinger Bands
* Bollinger Bands are a type of price envelope developed by John Bollinger
* Bollinger Bands are envelopes plotted at a standard deviation level above and below a simple moving average of the price. Because the distance of the bands is based on standard deviation, they adjust to volatility swings in the underlying price.
* Bollinger Bands use 2 parameters, Period and Standard Deviations, StdDev. The default values are 20 for period, and 2 for standard deviations, although you may customize the combinations.
* Bollinger bands help determine whether prices are high or low on a relative basis. They are used in pairs, both upper and lower bands and in conjunction with a moving average. Further, the pair of bands is not intended to be used on its own. Use the pair to confirm signals given with other indicators.
* "Distance from a moving average" or "standard deviation" apply the same concept
* Click [here](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/bollinger-bands#:~:text=Bollinger%20Bands%20are%20envelopes%20plotted,Period%20and%20Standard%20Deviations%2C%20StdDev.) for more detail


```R
v <- Delt(Op(df),Cl(df),k=1:3)
colnames(v) <-c("pcntOpCl1","pcntOpCl2","pcntOpCl3")
df2 <- cbind(df,v)
#head(df2)
```


```R
macd <- MACD(df2$AMZN.Adjusted, nFast = 12, nSlow = 26, nSig = 9, maType = "SMA", percent = FALSE)
rsi <- RSI(df2$AMZN.Adjusted, n = 14, maType = "SMA")

#tail(macd)
```


```R
#tail(rsi)
```


```R
d <- cbind(AMZN,macd,rsi)
d$SMA12 <- SMA(d$AMZN.Adjusted,12)
d$SMA26 <- SMA(d$AMZN.Adjusted,26)
d <- subset(d, select = -c(AMZN.Open,AMZN.High,AMZN.Low,AMZN.Close,AMZN.Volume))
#d[50:60]
```

### Learning objective 5: How to plot technical charts


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, subset = "last 3 months")
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, subset = "2007::2008-01")
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, theme = chartTheme("white"))
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, subset = "2016::2018-12", TA = c(addVo(), addBBands()))  #add volume and Bollinger Bands from TTR
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, subset = "2018::2018-12",bar.type='hlc', 
#            TA = c(addSMA(n=12,col="blue"),addSMA(n=26,col="red")),
#            theme = chartTheme("white"))  
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, subset = "2018::2018-12",bar.type='hlc', 
#            TA = c(addSMA(n=12,col="green"),addSMA(n=26,col="red"),
#                addMACD(),addRSI()),
#            theme = chartTheme("white"))  
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#barChart(AMZN,subset = "2018::2018-12",bar.type='hlc') 
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#candleChart(AMZN,subset = "2018::2018-06",multi.col=TRUE, theme='white')
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, subset = "2018::2018-06",theme="white",  TA="addVo();addBBands();addCCI()") 
```


```R
options(repr.plot.width = 6, repr.plot.height = 3)
#chartSeries(AMZN, subset = "2018::2018-06",
#            theme="white",  
#            TA="addVo();addBBands();addCCI(); 
#                addTA(OpCl(AMZN),col='blue', type='h')  ")
```

### Learning objective 6: Develop your trading strategy & signals

#### MACD & RSI trading rule



```R
macd <- MACD(AMZN$AMZN.Adjusted, nFast = 12, nSlow = 26, nSig = 9, maType = "SMA", percent = FALSE)
rsi <- RSI(AMZN$AMZN.Adjusted, n = 14, maType = "SMA")
#tail(macd)
#tail(rsi)
```

Here we assume no transaction cost.


```R
macd <- MACD(AMZN$AMZN.Adjusted, nFast = 12, nSlow = 26, nSig = 9, maType = "SMA", percent = FALSE)
rsi <- RSI(AMZN$AMZN.Adjusted, n = 14, maType = "SMA")

# Strategy 1: if macd>signal, enter and stay in the market. If macd<signal, exit the market.
strategy1 <- ifelse ((macd$signal < macd$macd) , 1, 0)
strategy1[is.na(strategy1)] <-0

# Strategy 2: if overbought, enter and stay in the market.
strategy2 <- ifelse ((macd$signal < macd$macd) & (rsi$rsi > 70), 1, 0)
strategy2[is.na(strategy2)] <-0

# Strategy 3: if oversold, enter and stay in the market.
strategy3 <- ifelse ((macd$signal > macd$macd) & (rsi$rsi < 30), 1, 0)
strategy3[is.na(strategy3)] <-0


# Buy-and-hold: keep it all time. So "1", not "0"
bh_strategy <- rep(1,dim(macd)[1])
```

### Learning objective 7: Backtesting

#### Annualized return
* An annualized total return is the average amount earned by an investment each year over a given time period.

#### Sharpe Ratio
* [Sharpe Ratio](https://en.wikipedia.org/wiki/Sharpe_ratio)
* [Annualized Sharpe Ratio](https://www.rdocumentation.org/packages/PerformanceAnalytics/versions/2.0.4/topics/SharpeRatio.annualized#:~:text=The%20annualized%20Sharpe%20ratio%20is,standard%20deviation%20of%20excess%20return.)
* Usually, any Sharpe ratio greater than 1.0 is considered acceptable to good by investors. A ratio higher than 2.0 is rated as very good. A ratio of 3.0 or higher is considered excellent. A ratio under 1.0 is considered sub-optimal.
* "Lag": Since we are working with Closing prices, we can BUY or SELL on our signal the next day only


```R
# Put in a function
backtest <- function(df,from_date,to_date,strategy,strategy_name){
    trade_return <- rtn.daily[index(rtn.daily)<=to_date & index(rtn.daily)>=from_date]*lag(strategy, na.pad = FALSE)
    cumm_return <- Return.cumulative(trade_return)
    annual_return <- Return.annualized(trade_return) 
    summary(as.ts(trade_return))
    SharpeRatio <- SharpeRatio(as.ts(trade_return), Rf = 0, p = 0.95, FUN = "StdDev")
    SharpeRatioAnnualized <- SharpeRatio.annualized(trade_return, Rf = 0)
    out <- as.data.frame(c(cumm_return,annual_return,SharpeRatio,SharpeRatioAnnualized))
    out <- round(out,2)
    colnames(out) <- strategy_name
    row.names(out) <- c('Cumulative Return','Annualized Return','Sharpe Ratio','Annualized Sharpe Ratio')
    
  return( out )
    }

# Strategy 1
strategy1_performance <- backtest(AMZN, from_date = '2007-01-01', to_date = '2015-12-31', strategy1,"Strategy1")
strategy1_performance

# Strategy 2
strategy2_performance <- backtest(AMZN, from_date = '2007-01-01', to_date = '2015-12-31', strategy2,"Strategy2")
strategy2_performance

# Strategy 3
strategy3_performance <- backtest(AMZN, from_date = '2007-01-01', to_date = '2015-12-31', strategy3,"Strategy3")
strategy3_performance


# Buy-and-hold strategy
BH_backtest <- function(df,from_date,to_date,strategy_name){
    trade_return <- rtn.daily[index(rtn.daily)<=to_date & index(rtn.daily)>=from_date]
    cumm_return <- Return.cumulative(trade_return)
    annual_return <- Return.annualized(trade_return) 
    summary(as.ts(trade_return))
    SharpeRatio <- SharpeRatio(as.ts(trade_return), Rf = 0, p = 0.95, FUN = "StdDev")
    SharpeRatioAnnualized <- SharpeRatio.annualized(trade_return, Rf = 0)
    out <- as.data.frame(c(cumm_return,annual_return,SharpeRatio,SharpeRatioAnnualized))
    out <- round(out,2)
    colnames(out) <- strategy_name
    row.names(out) <- c('Cumulative Return','Annualized Return','Sharpe Ratio','Annualized Sharpe Ratio')
     
  return( out )
    }

buy_and_hold_performance <- BH_backtest(AMZN, from_date = '2007-01-01', to_date = '2015-12-31',"Buy & Hold Strategy")
buy_and_hold_performance
```


<table>
<thead><tr><th></th><th scope=col>Strategy1</th></tr></thead>
<tbody>
	<tr><th scope=row>Cumulative Return</th><td>1.23</td></tr>
	<tr><th scope=row>Annualized Return</th><td>0.09</td></tr>
	<tr><th scope=row>Sharpe Ratio</th><td>0.03</td></tr>
	<tr><th scope=row>Annualized Sharpe Ratio</th><td>0.33</td></tr>
</tbody>
</table>




<table>
<thead><tr><th></th><th scope=col>Strategy2</th></tr></thead>
<tbody>
	<tr><th scope=row>Cumulative Return</th><td>-0.01</td></tr>
	<tr><th scope=row>Annualized Return</th><td> 0.00</td></tr>
	<tr><th scope=row>Sharpe Ratio</th><td> 0.00</td></tr>
	<tr><th scope=row>Annualized Sharpe Ratio</th><td>-0.01</td></tr>
</tbody>
</table>




<table>
<thead><tr><th></th><th scope=col>Strategy3</th></tr></thead>
<tbody>
	<tr><th scope=row>Cumulative Return</th><td>0.73</td></tr>
	<tr><th scope=row>Annualized Return</th><td>0.06</td></tr>
	<tr><th scope=row>Sharpe Ratio</th><td>0.04</td></tr>
	<tr><th scope=row>Annualized Sharpe Ratio</th><td>0.55</td></tr>
</tbody>
</table>




<table>
<thead><tr><th></th><th scope=col>Buy &amp; Hold Strategy</th></tr></thead>
<tbody>
	<tr><th scope=row>Cumulative Return</th><td>16.47</td></tr>
	<tr><th scope=row>Annualized Return</th><td> 0.37</td></tr>
	<tr><th scope=row>Sharpe Ratio</th><td> 0.06</td></tr>
	<tr><th scope=row>Annualized Sharpe Ratio</th><td> 0.88</td></tr>
</tbody>
</table>




```R

```


```R

```
