# HVAC setpoint explained simply

**How it connects to the last lab:** lab 2 gave us a "comfort calculator" (PMV). Here we use that calculator again and again, like a thermometer for *feelings*, to decide how much to heat or cool.

## Key terms

* **HVAC** (Heating, Ventilation and Air Conditioning): the machines that warm, cool and refresh the air in a building
* **PMV** (Predicted Mean Vote): the average "how warm do I feel" vote of a group: -3 cold ... **0 just right** ... +3 hot
* **PPD** (Predicted Percentage of Dissatisfied): how many out of 100 people would complain
* **Category II** (comfort class of the standard): the "good enough" zone: PMV between **-0.5 and +0.5**
* **ta** (air temperature): what the thermometer on the wall says
* **tmr** (mean radiant temperature): how warm the **walls and windows** are (you feel them like a campfire or a cold window)
* **v** (air speed): how fast the air moves past you; a fan makes it bigger
* **RH** (relative humidity): how "wet" the air is, in %
* **clo** (clothing unit): how warm your clothes are (0.5 = light summer clothes, 1.0 = winter sweater)
* **met** (metabolic rate): how fast your body's engine runs (1.2 = sitting at a desk)
* **setpoint** (the target): the temperature you tell the heater to hold

# Part 0: What is HVAC?

**HVAC** = **H**eating + **V**entilation + **A**ir **C**onditioning. It is the team of machines that keeps a building pleasant.

* **H**eating: add warmth in winter — like a campfire inside a pipe
* **V**entilation: swap stale air for fresh air — like opening a window, but with a fan
* **A**C: remove heat (and water) in summer — like a fridge for a whole room

## The pieces

* **Boiler / heat pump / chiller** make the hot or cold water or air.
* **Ducts and pipes** carry it around, like the veins in a body.
* **The thermostat** (a sensor plus a brain) decides when to switch things on.

![How heat and cold travel from the machines to the room](figures/hvac-system.svg)

*Figure: How heat and cold travel from the machines to the room*

![The air handling unit: a box that cleans, warms, cools and pushes the air](figures/ahu.svg)

*Figure: The air handling unit: a box that cleans, warms, cools and pushes the air*

## Words you will see

* **Setpoint** = the number you wish for, "keep it at 23 degC".
* **Deadband** = a small gap where nothing switches on. Like not putting on and taking off your jacket every minute.
* **Thermostat vs PMV:** a normal thermostat looks at **one** thing, the air temperature. But **you** feel six things: air temperature, wall temperature, air speed, wetness, clothes and activity. PMV is one number that mixes all six. A smart controller uses PMV to find the **cheapest** setting that people still like.

![The thermostat idea: measure, compare with the target, act](figures/control-loop.svg)

*Figure: The thermostat idea: measure, compare with the target, act*

![A small gap around the target stops constant switching](figures/deadband.svg)

*Figure: A small gap around the target stops constant switching*

![Six things decide if a person feels comfortable](figures/pmv-six-factors.svg)

*Figure: Six things decide if a person feels comfortable*

![Your body is a little heater that gives heat away](figures/body-heat-exchange.svg)

*Figure: Your body is a little heater that gives heat away*

![From cold to hot: the comfort scale](figures/pmv-scale.svg)

*Figure: From cold to hot: the comfort scale*

![Cold windows make you feel cold even in warm air](figures/radiant-cold-window.svg)

*Figure: Cold windows make you feel cold even in warm air*

## Why comfort and energy are linked

Every degree of extra heating costs roughly **6 to 10 %** more energy (a common rule of thumb; it depends on the building). So if we can keep people happy at 21 degC instead of 23 degC, we **save energy for free**. That is the whole point of this sheet.

![From a simple switch to a learning controller](figures/control-levels.svg)

*Figure: From a simple switch to a learning controller*

**How to read a PMV number:** -3 cold, -2 cool, -1 slightly cool, **0 just right**, +1 slightly warm, +2 warm, +3 hot. **PPD** never goes below 5 %, because you can never please everybody.

# Part 1: Can a fan let the room be warmer?

**Idea.** Moving air takes heat off your skin, the way you feel cooler when you blow on hot soup. So with a fan we can set the air temperature **higher** and feel the **same**.

**Assumptions (summer office):** light clothes (clo 0.5), desk work (met 1.2), RH 50 %, walls 1 degree warmer than the air.

**Recipe:**
1. Still air (0.1 m/s) at **25 degC**: write down the comfort vote.
2. Turn the air speed up from 0.1 to 0.8 m/s.
3. For each speed, find the air temperature that gives **the same vote** as in step 1.

![A fan makes you feel cooler, so the room can be warmer](figures/ceiling-fan.svg)

*Figure: A fan makes you feel cooler, so the room can be warmer*

    Vote with still air at 25 degC: PMV = 0.278
    

    
![png](figures/output_20_0.png)
    

**What this means.**
* With the fan at 0.8 m/s the room can be **27.3 degC instead of 25 degC**, that is **2.3 degrees warmer** for the same feeling.
* The first push of air (0.1 to 0.2 m/s) buys **0.78 degrees**. The last push (0.7 to 0.8) buys only **0.13**. The fan has less and less to give, like the first bite of a cake tasting best. That is why ceiling fans run gently (0.3 to 0.6 m/s).
* **Energy:** 2 degrees warmer cooling target is roughly **12 to 20 % less cooling energy** (rule of thumb), and a ceiling fan only uses a few tens of watts.
* The third chart warns us: if we turn the fan on **and keep 25 degC**, the vote drops to **-0.65**, which means people get a bit chilly. We would waste energy over-cooling.

# Part 2: When does the building feel bad on its own?

**Idea.** We have a file with one row for each hour of a spring/autumn day: air temperature, wall temperature and humidity. **No heating or cooling is running.** For each hour we ask the comfort calculator for a vote, then mark the hours outside the "good" zone (-0.5 to +0.5).

**Assumptions for the people** (the sheet does not say): light indoor clothes for a transition day, clo 0.7, desk work (met 1.2), still air (0.1 m/s).

    too cold hours: [0, 1, 2, 3, 4]
    too warm hours: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    Comfortable 9 of 24 hours. Worst PMV 1.35 at hour 13, coldest PMV -0.69 at hour 2
    

    
![png](figures/output_24_0.png)
    

**What this means.**
* Only **9 of 24 hours** are fine by themselves. The building needs help.
* **Night, hours 0 to 4: too cold** (PMV -0.52 to -0.69). The air is about 20 degC and a bit damp. Hour 2 is the worst, and 15 out of 100 people would complain.
* **Daytime, hours 9 to 18: too warm.** The sun heats the air to 28 degC and the **walls even more** (29.2 degC at hour 13). The vote reaches **+1.35** and **43 out of 100** people would complain.
* **Good hours:** 5 to 8 and 19 to 23. At hour 7 the vote is exactly 0.00, perfect. In these hours the HVAC should simply stay **off**.
* **The walls matter:** in the afternoon the walls are warmer than the air, so the room feels hotter than the wall thermometer says. A thermostat that only reads the air would be fooled.
* The same day needs **a little heating at night and cooling (or fans) in the afternoon**. A simple "winter mode / summer mode" switch would waste energy.

    clo 0.5: 16 hours outside comfort   too cold [0, 1, 2, 3, 4, 5, 6, 22, 23]   too warm [11, 12, 13, 14, 15, 16, 17]
    clo 0.7: 15 hours outside comfort   too cold [0, 1, 2, 3, 4]   too warm [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    clo 1.0: 13 hours outside comfort   too cold []   too warm [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    

**What this means.** Thin clothes (0.5) make the cold hours longer (hours 0 to 6, 22, 23). A winter sweater (1.0) removes the cold hours but makes hours 8 to 20 too warm. **Clothes change the answer**, so a smart system should know what people wear (for example from the season).

# Part 3: The lowest heating temperature that is still comfy

**Idea.** In a very cold winter the **walls and windows are cold** (here 17 degC) and the heater can only control the **air**. Cold walls steal warmth from you, like standing next to a cold window. We ask: *what is the lowest air temperature that still gives PMV >= -0.5?* Heating more than that is wasted energy.

**Assumptions:** winter clothes (clo 1.0), desk work (met 1.2), RH 40 %, still air (0.1 m/s), walls at 17 degC.

We solve it in two ways:
* **While loop** (a simple controller): start cold, raise the temperature in small 0.05 degree steps until the vote reaches -0.5.
* **Root finder** (`brentq`): jumps straight to the exact answer, like guessing a number with "higher / lower" hints but smartly.

    while loop : 21.30 degC after 226 small steps
    root finder: 21.265 degC
    PMV there = -0.500, PPD = 10.2 %
    Fixed 23 degC would give PMV = -0.30, PPD = 6.9 %
    Saving versus the fixed 23 degC: 1.74 K
    

    
![png](figures/output_30_0.png)
    

**What this means.**
* The lowest comfortable air temperature is about **21.3 degC**. The vote is right at -0.50, and about 10 out of 100 people would complain. This is the sheet's own example (21.3 degC instead of the usual 23 degC).
* At the fixed **23 degC** the vote is **-0.30**: people are comfortable, but we heated **1.7 degrees more than needed**. With the 6 to 10 % per degree rule that is roughly **10 to 17 % less heating energy** for the same comfort.
* Both ways agree: the loop needed **226 tiny steps**, the root finder needed only a handful of tries.
* Real controllers keep a small safety margin (for example aim for -0.4) because sensors are never perfect.

    
![png](figures/output_32_0.png)
    

**What this means.**
* **Warm walls save energy:** every +1 degree on the walls lets the air be about **0.8 degree cooler** (from 23.7 degC with 14 degC walls to 18.0 degC with 21 degC walls). Better windows or insulation can beat simply turning the heater up.
* **Clothes are free heating:** going from clo 1.0 to 0.8 (a lighter sweater) forces the air to be about **2.8 degrees warmer**. Wearing the sweater costs nothing.
* If the walls are warm enough (about 15 degC and up with winter clothes) the fixed 23 degC is already **too high**; below that (14 degC walls) we actually need more than 23 degC.

# Part 4: The same question in different seasons

People dress differently and the walls behave differently in each season. For each season we:

1. Find the **comfort band**: the lowest and highest air temperature that stay inside PMV -0.5 to +0.5.
2. Count how many hours of our CSV day would feel bad **if people wore that season's clothes**.

* summer: clo 0.5, met 1.2, RH 50 %, v 0.1, walls tmr air + 1 degree (sunny walls)
* autumn / spring: clo 0.7, met 1.2, RH 50 %, v 0.1, walls tmr same as air
* winter: clo 1.0, met 1.2, RH 40 %, v 0.1, walls tmr 17 degC (cold windows)
* winter, heavy clothing: clo 1.2, met 1.2, RH 40 %, v 0.1, walls tmr 16 degC

    
![png](figures/output_35_0.png)
    

**What this means.**
* **The lowest comfortable temperature changes with the season:** 22.4 degC (summer), 21.3 degC (autumn/spring), 21.3 degC (winter, 17 degC walls) and 19.2 degC (winter with heavy clothes and 16 degC walls). **One fixed setpoint for the whole year can never be the cheapest.**
* **Summer has the narrowest band** (3.3 degrees, from 22.4 to 25.7 degC). Light clothes leave little room, which is where fans (Part 1) help.
* **Read winter rows for their LOWER limit only.** Their upper limits (29.8 and 28.6 degC) pretend the walls stay cold while the air is very hot, which does not happen in real buildings.
* **Bad hours on our day:** 16 (summer clothes), 15 (autumn), 13 (winter clothes), 15 (heavy winter clothes). Whatever people wear, the building fails for more than half of the day by itself, so it needs real HVAC help in both directions.
* **Two different winter assumptions, both fine:** heavier clothes and colder walls give a lower setpoint (19.2 degC vs 21.3 degC). The report should always say which assumptions were used.

# One-page summary

* Part 1: +2.3 K at 0.8 m/s: a fan lets us keep the room about 2 degrees warmer, with smaller and smaller gains
* Part 2: 9 of 24 h comfortable: night is slightly cold, afternoon is hot because the walls heat up
* Part 3: 21.3 degC instead of 23 degC: the smart setpoint saves about 1.7 degrees of heating
* Part 4: band 3.3 K (summer) to 8.5 K (winter): clothes, season and wall temperature all move the best setpoint
