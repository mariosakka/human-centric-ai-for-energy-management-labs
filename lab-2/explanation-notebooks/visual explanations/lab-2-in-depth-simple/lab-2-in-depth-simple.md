# Both sheets explained simply

- **1** (sheet *Psychrometrics challenge*): "How much **water** hides in the air, and how much **energy** does the air carry?" — **Part A**
- **2** (sheet *Lab 2*): "Will a **person** feel comfortable in that air?" — **Part B**

**How they connect:** sheet 1 is about the **air**, sheet 2 is about the **person standing in the air**. The amount of water in the air that you find in Part A is also needed by the body calculation in Part B.

# Part A: Sheet 1, the air and its hidden water

> **Moist air**: the air around us: **dry air plus a little invisible water** (water vapour).

> **Psychrometrics**: the science of "how much water is in the air".

## A1. How much does the air in a room weigh?

Air feels like nothing, but it has weight. The room is 6 m × 4 m × 3 m, at 25 °C and normal pressure.

> **Pressure** (Pa): how hard the air pushes on things. It is measured in **pascals** (Pa), and normal air pressure is 100 000 Pa (1 bar).

> **Ideal gas**: a gas simple enough to follow the "ideal gas law" (pressure × volume = mass × R × temperature). We treat air like that.

**Recipe** (the ideal gas law):

- $p$ = 100 000 Pa and $V$ is the volume of the room (72 m³)
- $R$ = 287 J/(kg·K) is a number for air
- $T$ is the temperature in kelvin (box below)

> **Kelvin** (K): the temperature scale used in gas formulas; always add 273.15 to the °C value.

![Even air has weight: this room holds as much air as a person weighs, more than once](figures/air-parcel-room.svg)

*Figure: Even air has weight: this room holds as much air as a person weighs, more than once*

    The room has 72 m3 of air. It weighs 84.1 kg (about 1.2 adults!). Density = 1.17 kg/m3
    

    
![png](figures/output_5_1.png)
    

**Reading it.** When air gets warm it spreads out, so each cubic metre holds less stuff and weighs less. That is why warm air rises (hot-air balloons!). Our room's air weighs about **84 kg**.

## A2. The sponge: warm air holds much more water

The sheet gives a table: for each temperature, the biggest water pressure the air can hold. Between table rows we draw a straight line (*interpolation*).

> **Saturation pressure** $p_{sat}$ (Pa): the **biggest** water pressure the air can hold at a given temperature.

**What does "100 % humidity" mean?** Think of the air as a sponge that can soak up water vapour. How much it can hold depends on the temperature: that biggest amount is $p_{sat}$.

> **Partial vapour pressure** $p_v$ (Pa): the water that is really in the air, how hard the water part alone pushes. More water means a bigger number.

> **Relative humidity** $\varphi$: how full the sponge is, $p_v$ divided by $p_{sat}$:

- **100 %** = the sponge is **completely full** at this temperature. One more drop would not fit, it turns into liquid (dew, fog, a cloud). "100 % humidity", "100 % relative humidity" and "saturated" all mean this same thing.
- It does **not** mean the air is made of water. A full sponge at 10 °C only holds a few grams of water per kilogram of air.
- **60 %** = the sponge is 60 % full. **0 %** = completely dry.
- The **black curve** in the chart below is the biggest amount the air can hold, so it is the **100 % line**. The dashed lines are 60 % and 30 % full. Above the curve there is no room: the water would have to become liquid. Below the curve there is still space.
- The sponge changes size with the temperature. The sheet's summer air (30 °C) is only 60 % full. Cool it to 21.4 °C and the same water fills the whole (smaller) sponge: 100 %. That temperature is the dew point (A4).

> **Dew point**: the temperature where the air gets so cold that its sponge is full and drops appear.

![The warmer the air, the more water it can hold; cool it and it overflows at the dew point](figures/vapour-pressure-dew-point.svg)

*Figure: The warmer the air, the more water it can hold; cool it and it overflows at the dew point*

    
![png](figures/output_9_0.png)
    

**Reading it.** At 0 °C the air can hold 611 Pa of water, at 30 °C it can hold 4247 Pa, which is about **7 times more**. The orange arrow shows how much room is left in the summer air and the horizontal arrow shows how far it has to cool to be full. Everything else in Part A comes from this picture.

## A3. Summer day vs winter day (the 5 steps of the sheet)

**Summer:** 30 °C and 60 % humidity. **Winter:** 0 °C and 85 % humidity. Both at 1 bar.

1. **Sponge size** $p_{sat}$: look it up in the table.
2. **How much water is really there:** $p_v = \varphi \cdot p_{sat}$ (60 % of the sponge).
3. **Humidity ratio $x$ (box below):** $x = 0.622\,\dfrac{p_v}{p - p_v}$ (0.622 because water molecules are lighter than air molecules).
4. **Dew point:** find the temperature whose sponge size equals $p_v$ (look the table up **backwards**).
5. **Enthalpy $h$ (box below):** $h = t + x\,(2500 + 1.84\,t)$ (warmth + hidden energy).

> **Humidity ratio** $x$ (g of water per kg of dry air): how many grams of water are mixed into each kilogram of dry air.

> **Enthalpy** $h$ (kJ per kg): the energy the air carries (a kilojoule, kJ, is 1000 joules, a unit of energy).

> **Latent heat** (2500 kJ/kg): what it costs to turn 1 kg of water into vapour.

> **Specific heat** of water vapour (1.84 kJ/(kg·K)): how stubborn water vapour is about warming (explained below).

    
![png](figures/output_12_0.png)
    

    
![png](figures/output_13_0.png)
    

**Reading it.** Winter feels "85 % wet", but the cup is tiny, so there are only **3.2 g** of water per kg of air. Summer is "only 60 %" but the cup is huge, so there are **16.3 g**, five times more. **Lesson: the percentage alone lies; the grams tell the truth.**

## Why do we measure water in the air with *pressure* and not in kilograms?

**We use both! They are the same thing said in two ways.**

Imagine a box of tiny bouncing balls (the water molecules). The more balls, the harder they bump the walls of the box. **That bumping is the pressure.** So *more pressure = more water*. Pressure is just a way to count the water without a scale.

> **Vapour density** $\rho_v$ (kg/m³): the kilograms of vapour in each m³ of air.

The formula that links the two is $p_v = \rho_v \cdot R_v \cdot T$: pressure = ($\rho_v$) × a fixed number × the temperature. And the humidity ratio $x$ is just "kg of water ÷ kg of dry air", exactly the number you described:

**Why use pressure at all?**
- The "sponge is full" rule is written in pressure: the air is full when $p_v = p_{sat}$, so a look-up table does the job. Relative humidity is simply $p_v / p_{sat}$.
- The dew point is also found with that table.

**Why also use kilograms ($x$)?**
- $x$ **does not change** when you only warm up or cool down the air. The water is still the same water! That makes it the honest number for energy and for "how much water do we need to add or remove".
- The percentage (relative humidity) *does* change when you warm the air, as you can see below.

    vapour : 18.21 g per m3     dry air: 1.120 kg per m3
    x = rho_v/rho_a = 16.26 g/kg      formula 0.622*pv/(p-pv) = 16.26 g/kg   (same thing)
    

    
![png](figures/output_16_1.png)
    

**Reading it.** While we warm the same air, the water in it ($x$ in g/kg and $p_v$ in Pa) **stays the same**. But the percentage falls from 80 % (at 25 °C) to 35 % (at 40 °C), because warm air has a bigger sponge. So the percentage is a bit of a trickster; grams per kg (and pressure) tell the truth.

### Heating the air: where does the extra air go?

Here are two sentences that sound like they fight each other:
1. *Warm air spreads out, so a cubic metre has fewer air and water bits in it.*
2. *The grams of water per kg of air ($x$) and the dew point do not change when we only warm the air.*

They don't fight, because **$x$ and the dew point do not count "how many bits per cubic metre"**. $x$ asks: *for each kg of dry air that is here, how much water is mixed in?* Heating doesn't change the mix, only how tightly the bits are packed. What happens to the pressure depends on whether the extra space has anywhere to go.

**A. A real room (it has cracks and gaps).** The warm air spreads out and some of it **leaves through the cracks**. It leaves with the same mix of water and air it had before (look at the dots in the middle picture: 10 grey for every 1 blue, outside and inside). The air that stays has the same mix, so $x$ is the same. The pressure stays at 1 bar, so the water's share of the pressure ($p_v$) stays the same, and so does the dew point. There is less of everything per cubic metre, so the humidity percentage drops (the sponge got bigger).

**B. An isolated room (sealed shut).** Nothing can leave. The same bits are now moving faster and bang into the walls harder, so the **pressure goes up**. This is not magic, it is the gas law $p=\rho R T$: same bits, hotter, more pressure. From 30 °C to 40 °C the pressure goes up by 3.3 % (1 bar becomes 1.033 bar; a closed bottle left in the sun can burst). The water's share of the pressure goes up by the same 3.3 %, so $p_v$ goes from 2548 to 2632 Pa. The grams of water per kg of air ($x$) is exactly the same, but the dew point rises a little, **from 21.4 °C to 21.9 °C**, because the water pushes harder.

The first picture shows the three rooms (with extra dots so you can see them), the second compares the numbers.

![Heating a room: the water stays, so only the percentage drops](figures/sealed-vs-leaky-room.svg)

*Figure: Heating a room: the water stays, so only the percentage drops*

    
![png](figures/output_20_0.png)
    

    
![png](figures/output_21_0.png)
    

## A4. Dew point: when the sponge gets full

Imagine the air in the summer day getting cooled down **without adding or removing water**. The amount of water stays the same ($p_v$ is a straight line in the chart), but the sponge gets smaller (the black 100 % curve comes down towards it). At some temperature the sponge is exactly full, 100 %. That is the **dew point**. Cooler than that, water drops out (fog, dew, a wet cold glass).

**The dew point as a formula.** The dew point is the temperature where the sponge size ($p_{sat}$) is exactly the amount of water in the air ($p_v$):

So we use the sponge-size table **backwards**: we start from the water amount $p_v$ and read off a temperature. The sheet's Antoine equation (a formula fitted to measured values), $p_{sat}(t)=e^{16.6536-4030.183/(t+235)}$ in kPa, can also be solved for the temperature:

If you only know the air temperature and the humidity percentage, first find $p_v=\varphi\cdot p_{sat}(t)$, then use the formula.

**Why the dew point doesn't care about the air temperature.** "Sponge size" means two things:
- the **table** of sponge sizes for every temperature, which is a fixed fact about water;
- the sponge size **right now** at the air's temperature, one line of that table.

The dew point reads the table backwards starting from $p_v$, so it never uses the air's own temperature. Warm the air without adding water: the sponge right now gets bigger (the percentage drops), but the water amount and the table stay the same, so the dew point stays the same. It only moves when the water amount moves: more evaporation raises it, condensation (vapour turning into drops, explained below) lowers it, and a sealed room that is heated raises it a little (see the section on heating the air above). More water in the air always means a higher dew point.

![Cooling humid air: nothing happens until it is full, then drops appear](figures/humidity-ratio-and-dew-point.svg)

*Figure: Cooling humid air: nothing happens until it is full, then drops appear*

![The air map: up is more water, right is warmer](figures/psychrometric-chart.svg)

*Figure: The air map: up is more water, right is warmer*

    
![png](figures/output_25_0.png)
    

**Reading it.** Circle = the air now. Square = its dew point, always sitting **on the black 100 % curve**. The arrow is the cooling. In summer the air needs to cool **8.6 °C** (to 21.4 °C) before drops form, so a cold wall or an air-conditioner pipe at 15 °C will **drip**. In winter only 2.2 °C below zero is needed, so you get frost on a cold window. The winter arrow is short even though 85 % sounds wetter than 60 %: the winter sponge is small.

## What is condensation?

> **Condensation**: when invisible water in the air turns into tiny drops of liquid water.

You have seen it:
- the drops on the **outside of a cold glass** of lemonade,
- the **mirror fogging up** after a hot shower,
- **dew** on the grass in the morning, **fog** and **clouds**,
- water on a **window** on a cold day.

**Why it happens:** remember the sponge. Cold air has a *small* sponge. If air touches something cold, its sponge shrinks until it can't hold all its water any more. The extra water **squeezes out as drops**. The temperature where this starts is the **dew point**.

- Surface **warmer** than the dew point → stays dry.
- Surface **colder** than the dew point → drops appear.

When water turns from vapour into liquid it **gives out heat** (the hidden energy from before). An air conditioner works like a cold glass: it makes water drip out of the air, which both cools **and dries** the room.

**Two "water in the air" numbers appear in the chart below, and they are different.**
> **Water the air really has** ($x$, orange flat line): if nobody adds or removes water, it **doesn't change when the temperature changes**.

> **Most water the air could hold** ($x_{sat}(t)$, blue curve): the size of the sponge at each temperature, written in grams per kg of air, so it **does change with temperature**: warm air has a big sponge, cold air a small one. It is the 100 % line of A2 again, not a measure of the water that is there.

Cooling the air moves it **left along the flat line** (same water) until the line touches the curve: the dew point, the sponge is full. Cooling further, the sponge becomes smaller than the water inside, so the extra water **squeezes out as drops** and the air's own water now goes down along the curve. **The air's water only changes with temperature after the drops start.**

    At 15 degC the air can hold only 10.81 g/kg, it carries 16.26 g/kg
    -> 5.45 g of every kg turns to liquid; for the room's 84.14 kg of air that is 459 g of water
    -> condensing releases 13.6 kJ per kg of air, 1146 kJ in the room
    

    
![png](figures/output_29_1.png)
    

**Reading it.** Summer air (30 °C, 60 %) has a dew point of 21.4 °C. If it touches something at 15 °C, its sponge only holds 10.8 g per kg instead of 16.3 g, so about 5.5 g per kg turns into drops. For all the air in the room that is about **half a litre of water**, a small bottle! The green area on the chart is the water that has to leave the air. The flat orange line is the water the air really has (it stays the same while cooling), the blue curve is the sponge size at each temperature, and the two arrows are the two stages: along the flat line to the dew point, then along the curve while drops form.

## What is specific heat?

> **Specific heat**: how "stubborn" a material is about getting warm. It is the energy needed to warm **1 kg** of something by **1 degree**.

Think of two pots on a stove: one with a little oil and one with the same weight of water. The oil gets hot much faster. Water is "stubborn": it needs a lot of energy for every degree, so it also stays warm for a long time.

- **Dry air**: **1.0** (exactly 1.006) — warms up easily
- **Water vapour**: **1.84** — in between
- **Liquid water**: **4.19** — very stubborn

**Where do we use it?** In the **energy of the air** $h$:

The "1" is the specific heat of dry air, the "1.84" the specific heat of vapour. The 2500 is **not** a specific heat: it is the big chunk of energy needed to turn 1 kg of liquid water into vapour (even without getting any warmer).

    
![png](figures/output_32_0.png)
    

![Water needs about 4 times more energy than air to warm up by one degree](figures/specific-heat.svg)

*Figure: Water needs about 4 times more energy than air to warm up by one degree*

    warm the room's air by 1 K :   84.6 kJ
    warm the same MASS of water:  352.5 kJ   (4.2 times more)
    h = 30.00 (dry air) + 0.90 (vapour warmth) + 40.66 (latent) = 71.56 kJ/kg
    with c_pa = 1.006 instead of 1: h = 71.74 kJ/kg (difference 0.25 %)
    

**Reading it.** Warming the air in the room by one degree takes about 85 kJ, but warming the same weight of water takes more than 350 kJ, about 4 times more. In the summer air's 71.6 kJ/kg: 30 is the warmth of the dry air, 0.9 the warmth of the water vapour and 40.7 the hidden energy. Using 1.006 instead of 1 changes the answer by a tiny 0.25 %, so the sheet just uses 1.

## A5. Enthalpy: the energy you can't feel

$h = \underbrace{t}_{\text{warmth (sensible)}} + \underbrace{x\,(2500 + 1.84\,t)}_{\text{hidden in water (latent)}}$

Think of **two piggy banks**: one holds the warmth you can feel with a thermometer, the other holds energy hidden in the water. An air conditioner has to empty **both**.

![Hot air carries two kinds of energy: warmth you feel and energy hidden in water](figures/enthalpy.svg)

*Figure: Hot air carries two kinds of energy: warmth you feel and energy hidden in water*

    
![png](figures/output_38_0.png)
    

**Reading it.** In summer, 42 of the 71.6 kJ/kg are hidden in the water, so cooling alone is not enough: you must also **dry** the air. In winter (0 °C) there is no warmth to count, so the whole 8.1 kJ/kg is hidden energy.

## A6. The whole day

The sheet gives 24 hourly temperatures and humidities (Bucharest, 8 August and 1 February). We repeat the 5 steps for every hour and plot the **grams of water per kg of air**.

    
![png](figures/output_41_0.png)
    

    Summer: water 8.5-14.8 g/kg, energy 41-60 kJ/kg
    Winter: water 3.5-4.8 g/kg, energy 10-19 kJ/kg
    

**Reading it.** The rings mark the highest and lowest points of each line. The summer air always carries much more water and energy than the winter air (roughly 3 to 4 times as much energy). That is why summer needs air-conditioning that **cools and dries**, while winter needs **heating** (and sometimes adding humidity). Notice that the summer energy peaks at 08:00, when the air is already warm and still very humid, and not at the hottest hour: section A7 explains why.

## A7. Which curves move together?

All the graphs above show the **same few things**, and they are linked, because most of them are **calculated from each other**. Only the air temperature $t$ and the humidity percentage $\varphi$ are measured. Here we look at the 24 hours of both days and check, one pair at a time, which curves rise and fall together, which are opposites and why.

> **Correlation** $r$ (the "friendship score"): a number from −1 to +1 that tells how two curves move together.

How to read it:
- **+1** = they rise and fall **together** (left plot: dots go up from left to right);
- **0** = **strangers**, no pattern (middle plot);
- **−1** = **opposites**, like a seesaw (right plot: dots go down).

    
![png](figures/output_44_0.png)
    

    
![png](figures/output_44_1.png)
    

**Map of who is calculated from whom** (an arrow means "is calculated from"):
1. **The water amount.** From $t$ and $\varphi$ we get $p_v$, and from $p_v$ alone we get **both** $x$ and the dew point. So $x$ and the dew point are the same information (one in g/kg, one in °C): they must have the same shape (section 3).
2. **The percentage.** $\varphi=p_v/p_{sat}(t)$ uses the temperature again. Warmer air has a bigger sponge, so with the same water the percentage goes **down** (section 2). The gap $t-t_{dp}$ says the same thing in degrees (section 4).
3. **The energy.** $h$ adds the warmth ($t$) and the hidden energy (from $x$), so it follows whichever moves more (section 5).

    
![png](figures/output_46_0.png)
    

### 2. Temperature and humidity percentage: a seesaw

Warm air has a bigger sponge. If no water is added, the sponge gets bigger but the water stays the same, so the percentage falls. Over a day the air warms from morning to afternoon, so the percentage should fall in those hours.

In the figure the coloured line is the temperature (left axis) and the dashed black line the humidity percentage (right axis). The wide pale arrows show the morning-to-afternoon stretch: **the temperature goes up, the percentage goes down**. Circles mark the highest and lowest hours.
- **Summer** ($r=-0.75$): the temperature climbs from 20.7 °C (05:00) to 27.9 °C (15:00) and the percentage drops from 89 % to 46 %. It is lowest (44 %) at 16:00, one hour after the warmest moment, and highest (91 %) at 04:00 when the air is only 21 °C. The seesaw is not perfect because the water in the air also changes during the day.
- **Winter** ($r=-0.89$): from 1.1 °C (07:00) to 7.9 °C (13:00) the percentage drops from 85 % to 69 %. It only swings between 66 and 87 %, because the warmer winter air also picks up some water (section 3).

    
![png](figures/output_48_0.png)
    

### 3. Dew point and grams of water: the same curve

The dew point is just the water amount ($p_v$) written as a temperature, and $x$ is the same amount written in grams per kg. So the two lines are copies of each other. In the first two panels the dashed line ($x$) sits on top of the solid line (dew point); the axes are scaled so you can see it. The dotted lines and circles mark the highest and lowest hours: **both turn at the same hour** ($r=1.00$).
- **Summer:** both highest at 02:00 (dew point 19.9 °C, 14.8 g/kg), both lowest at 24:00 (11.3 °C, 8.5 g/kg).
- **Winter:** both highest at 12:00 (3.1 °C, 4.8 g/kg), both lowest at 06:00 (−1.3 °C, 3.5 g/kg).

The right panel: all 48 hours lie on **one curve, the 100 % curve of A2** (the "full sponge" line). That is what the dew point means: air with this much water is exactly full at the temperature where it meets that curve. Summer is high on the curve (humid), winter low on it (dry).

    
![png](figures/output_50_0.png)
    

### 4. The gap to the dew point and the percentage

The gap $t-t_{dp}$ is how many degrees the air must cool before the sponge is full. A small gap means nearly full; **gap 0 means exactly 100 %** (the star). The dots fall on a line sloping down from the star ($r=-1.00$): the bigger the gap, the drier the air.
- **Summer night** (01:00 to 08:00): gap 1.5 to 3.6 °C, 80 to 91 %: nearly fog.
- **Summer afternoon** (12:00 to 16:00): gap 10.4 to 13.4 °C, 44 to 53 %: dry end of the line.
- **Winter**: gap 2.0 to 5.9 °C, 66 to 87 %: always close to fog, even though there is very little water in the air.

    
![png](figures/output_52_0.png)
    

### 5. Energy: does it follow the warmth or the water?

$h$ = warmth ($t$) + hidden energy (proportional to $x$), so it follows whichever of the two moves more. Each panel plots $h$ against one of them; the wide stripe is the trend and the label tells you if the dots make a tight line or a loose cloud.
- **Winter** ($r=0.99$ with $t$, $0.96$ with $x$): warmth and water rise together, so $h$ follows both. The warmth part moves 6.8 kJ/kg over the day, the hidden part only 3.3, so warmth leads.
- **Summer** ($r=0.33$ with $t$, $0.84$ with $x$): warmth and water are strangers ($r=-0.23$), because the humid hours are the cool night hours. The hidden part moves 16.1 kJ/kg and the warmth part only 8.6, so the **water leads**. The temperature panel is a cloud, the water panel a tighter line.
- **The circles in the summer panels:** at 08:00 the air is only 23.3 °C but its energy is the day's highest (60.4 kJ/kg), because it holds 14.6 g/kg of water. At 24:00 it is the coolest and driest hour, with the lowest energy (40.8 kJ/kg).

    
![png](figures/output_54_0.png)
    

# Part B: Sheet 2, will a person feel comfortable?

## B0. The big idea: your body is a little campfire

Your body **makes heat** all the time (even asleep). The room **takes heat away**. Think of a **bathtub**: the tap is the heat you make, the drains are the ways the room steals it.

- Drains take **exactly** what the tap gives → water level steady → you feel **just right**.
- Drains take **less** → level rises → you feel **hot**.
- Drains take **more** → level sinks → you feel **cold**.

The number that says "how high is the water level" is the **PMV** (Predicted Mean Vote). We then count how many people out of 100 would complain: the **PPD** (Predicted Percentage of Dissatisfied).

> **Metabolic rate**: how much heat your body makes (the tap). It is measured in **met**: 1 met is a person sitting quietly, about 58 W of heat for every square metre of skin (a **watt**, W, is energy per second).

![Six things decide if a person feels comfortable](figures/pmv-six-factors.svg)

*Figure: Six things decide if a person feels comfortable*

The six factors in the picture:

> **Air temperature** $t_a$ (°C): what a normal thermometer says.

> **Mean radiant temperature** $t_{mr}$ (°C): how warm the **walls and windows** are. You feel a cold window even when the air is warm.

> **Air speed** $v$ (m/s): how strong the breeze is. Wind steals heat.

> **Relative humidity** (%): how sticky the air is (Part A's sponge). Sticky air makes sweating less effective.

> **Clothing insulation** $I_{clo}$ (clo): how warm your clothes are, like a blanket around the bathtub. Measured in **clo** (0.5 = light summer clothes, 1 = a winter suit).

> **Activity**: the metabolic rate $M$ from above (sitting ≈ 1 met, running much more).

### What do PMV and PPD stand for?

A scientist called Fanger (Denmark, 1960s) put volunteers in special rooms, changed the temperature, wetness of the air, wind and clothes, and asked everybody to **vote** on a scale: −3 cold, −2 cool, −1 slightly cool, **0 just right**, +1 slightly warm, +2 warm, +3 hot.
> **PMV (Predicted Mean Vote)**: the *average* vote of a big group (add all votes, divide by the number of people); a *vote* is one person's answer. *Predicted* means we don't ask anyone: we **calculate** the vote with the body's heat balance (the bathtub: heat made minus heat lost).

> **PPD (Predicted Percentage of Dissatisfied)**: how many out of 100 would complain, meaning they feel **warm or hot (+2, +3) or cool or cold (−2, −3)**. Even when the *average* person is happy, some people are not, so it is never below 5 %: you can't please everyone.

> **ISO 7730** (ISO = International Organization for Standardization): the official rule-book that says how to calculate PMV and PPD.

> **ASHRAE 55** (American Society of Heating, Refrigerating and Air-Conditioning Engineers): a similar rule-book from a club of heating and cooling engineers.

## B1. Clothes are a guessing game

The clothes' outer surface has a temperature $t_{cl}$ that we don't know, but we need it to compute the heat that leaves through the clothes. And that heat itself depends on $t_{cl}$! A chicken-and-egg problem. The trick: **guess, improve, repeat** until the guess stops changing. The sheet asks us to count how many rounds it takes (we stop when the change is below 0.0015).

> **Iteration**: guess, improve the guess, repeat until the guess stops changing.

![More clothes or more movement means you feel warmer](figures/clothing-and-activity.svg)

*Figure: More clothes or more movement means you feel warmer*

![Guess, check, improve, repeat: the clothing-temperature game](figures/tcl-iteration.svg)

*Figure: Guess, check, improve, repeat: the clothing-temperature game*

    Outdoor: PMV = 1.767, PPD = 65.3 %, operative temperature = 30.25 degC, rounds of guessing = 8
    

    
![png](figures/output_62_1.png)
    

**Reading it.** The first guess is a bit off, then each round gets closer, like finding a hidden toy by being told "warmer, warmer, ...". We stop when the answer moves less than 0.0015 (that is 0.15 °C). The sheet's answer is **8 rounds**.

## B2. Where does the heat go? (the 6 drains)

The body loses heat through six paths. Each one is a heat flux (box below):

> **Heat flux** (W/m²): the heat per second flowing through one square metre of skin.

> **RL1**: water slowly seeping out through the skin

> **RL2**: sweating (only if you make more heat than when resting)

> **RL3**: water vapour you breathe out

> **RL4**: warm air you breathe out

> **RL5**: heat radiating from your clothes to the walls

> **RL6**: air carrying heat away from your clothes (breeze)

> **Thermal load** $L = M - RL1 - \dots - RL6$: what is left over in the body.

Then **PMV = (sensitivity) × L**, where the *sensitivity* is a fixed number that turns the left-over heat into a vote. Positive means heat piles up (hot), negative means too much leaves (cold).

![Your body is a little heater that gives its heat away in several ways](figures/body-heat-exchange.svg)

*Figure: Your body is a little heater that gives its heat away in several ways*

    
![png](figures/output_66_0.png)
    

**Reading it.** The body makes about 70 W/m² in both cases. Indoors, the drains take away almost exactly that (little is left over → PMV ≈ 0). Outdoors, the radiation and breeze drains (RL5, RL6) nearly vanish because the air is as warm as your clothes, so about 30 W/m² piles up → you feel hot.

## B3. From heat left over to a vote (PMV) and complaints (PPD)

- **PMV** scale: −3 cold, −2 cool, −1 slightly cool, **0 neutral**, +1 slightly warm, +2 warm, +3 hot.
- **PPD** is the % unhappy. Even at a perfect PMV = 0, 5 % of people complain (we are all different!).

> **Operative temperature** $t_o$: the "feels-like" temperature of the room: a mix of the air temperature and the wall temperature. It is printed below.

> **Comfort categories**: a room is called **category I** (very good) when PMV is within ±0.2, category II within ±0.5, category III within ±0.7.

![From cold to hot: the comfort vote](figures/pmv-scale.svg)

*Figure: From cold to hot: the comfort vote*

    
![png](figures/output_70_0.png)
    

**Reading it.** The curve is a bowl: lowest at 0 (5 %), rising fast on both sides. Outdoors (PMV 1.77) about **65 %** are unhappy; our indoor room (PMV −0.03) is at the bottom of the bowl, **5 %**.

## B4. Finding the right indoor temperature (the second half of the sheet)

We keep the same person (light clothes 0.5 clo, sitting 1.2 met, 60 % humidity, almost no breeze) and try air temperatures from 18 to 30 °C. In summer the walls are about 0.5 °C warmer than the air ($t_{mr} = t_a + 0.5$). We look for where **PMV stays between −0.5 and +0.5**.

    
![png](figures/output_73_0.png)
    

**Reading it.** The blue line climbs as the room gets warmer. The green zone is where people say "just right": about **23.0 to 26.1 °C**. We picked **24.5 °C** (air) / **25 °C** (walls): PMV = −0.03, PPD = 5 %, category I. Try clothes of 1.0 clo or activity of 2.0 met in the call above and watch the green zone slide down: **warmer clothes or more movement means you want a cooler room**.

## B5. Cheat-sheet

- **Water pressure, grams of water, dew point, energy for summer / winter day** (sheet 1): A3 results: 16.26 / 3.25 g/kg, 21.37 / −2.23 °C, 71.56 / 8.12 kJ/kg
- **Mass of air in the 6×4×3 m room** (sheet 1): 84.14 kg (1.17 kg/m³)
- **PMV, PPD, $t_o$, rounds (outdoor 30 / 30.5 °C)** (sheet 2): 1.767, 65.3 %, 30.25 °C, 8
- **Indoor state with −0.5 < PMV < 0.5** (sheet 2): 24.5 / 25 °C → PMV −0.03, PPD 5.0 %, $t_o$ 24.75 °C

**One sentence for each sheet:** *Sheet 1:* "Warm air has a big sponge, so summer air carries far more water and energy than winter air." *Sheet 2:* "Comfort is when the heat your body makes equals the heat the room takes away."
