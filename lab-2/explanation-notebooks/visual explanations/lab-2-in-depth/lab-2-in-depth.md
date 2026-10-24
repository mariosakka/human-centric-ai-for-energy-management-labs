# Lab 2 in depth: from the moist-air sheet to the comfort sheet

- **1** (sheet *Psychrometrics Study Sheet Challenge*): Describe a summer and a winter day in Romania: $p_{sat}$, $p_v$, $x$, $t_{dp}$, $h$, then the same for a whole day (24 h of Meteonorm data) — **Part A**
- **2** (sheet *AI for Energy Lab 2*): Code that returns PMV (Predicted Mean Vote), PPD (Predicted Percentage of Dissatisfied), operative temperature $t_o$, number of iterations, then find an indoor state with $-0.5<PMV<0.5$ — **Part B**

**How they connect.** Sheet 1 is about the *air* (how much water it holds, how much energy it carries). Sheet 2 is about the *person* in that air. The water-vapour pressure $p_v$ you compute in sheet 1 is exactly the $p_v$ that feeds two of the six body heat-loss paths in sheet 2.

Formulas come from the lecture slides. Added assumptions (for example an emissivity) are flagged.

# Part A: Sheet 1, the moist-air (psychrometrics) challenge

## A0. Vocabulary

- **Moist air**: The air around us: **dry air + water vapour**. We treat it as only these two ingredients. — -
- **Psychrometrics**: The study of the properties of moist air. — -
- **Ideal gas**: A gas simple enough to follow $pV = mRT$. Dry air, vapour and their mixture are all treated this way. — -
- **Dalton's law**: Total pressure = pressure of dry air + pressure of vapour: $p = p_a + p_v$. Each gas pushes as if it were alone. — Pa
- **Partial vapour pressure $p_v$**: The share of the total pressure that is due to water vapour. It measures **how much** water is in the air. — Pa
- **Saturation pressure $p_{sat}(t)$**: The **most** vapour pressure air can have at temperature $t$. Above it, water condenses. Rises quickly with $t$. — Pa
- **Relative humidity $\varphi$**: How full the air is: $\varphi = p_v / p_{sat}(t)$. — % (or fraction)
- **Humidity ratio $x$**: Mass of vapour per mass of **dry** air: $x = m_v/m_a = 0.622\,\dfrac{p_v}{p-p_v}$. — kg/kg (often g/kg)
- **Dew point $t_{dp}$**: The temperature to which you must cool the air, with no water added or removed, for it to become saturated (fog / dew). Defined by $p_{sat}(t_{dp}) = p_v$. — °C
- **Dry-bulb temperature**: The ordinary thermometer reading $t$. — °C
- **Wet-bulb temperature**: Reading of a thermometer wrapped in a wet cloth: evaporation cools it, more so in dry air. (Not needed for this sheet.) — °C
- **Enthalpy $h$**: Total **heat energy carried by 1 kg of dry air**: warmth (sensible) + energy hidden in the vapour (latent). $h \approx t + x(2500+1.84\,t)$. — kJ/kg
- **Specific heat $c$**: Energy to warm **1 kg** of a substance by **1 K**: $Q = m\,c\,\Delta T$. Dry air 1.006, vapour 1.84, liquid water 4.19. — kJ/(kg·K)
- **Latent heat of vaporisation**: Energy to turn 1 kg of liquid water into vapour with no temperature change (about 2500 kJ/kg). Released again when the vapour condenses. — kJ/kg
- **Condensation**: Water vapour turning into liquid. Starts when the air is cooled below its dew point ($p_v > p_{sat}$). — -
- **Vapour density $\rho_v$**: Kilograms of vapour per m³ of air, linked to pressure by $p_v = \rho_v R_v T$. — kg/m³

The constant 0.622 is the ratio of molar masses, water (18) / air (29). The 2500 kJ/kg is the energy needed to evaporate 1 kg of water, and 1.84 kJ/(kg·K) is the vapour's specific heat.

## A1. Lecture challenge: mass and density of the air in a room

Room 6 m × 4 m × 3 m, $p$ = 1 bar = 10⁵ Pa, 25 °C. Ideal gas law $pV = mRT$ with $R$ = 287 J/(kg·K) for air, $T$ in kelvin (the °C value plus 273.15).

![The air in a 6 × 4 × 3 m room: volume, mass and density](figures/air-parcel-room.svg)

*Figure: The air in a 6 × 4 × 3 m room: volume, mass and density*

    V = 72 m3   m = 84.14 kg   rho = 1.17 kg/m3
    

    
![png](figures/output_5_1.png)
    

**Reading it.** Same pressure, hotter air means the molecules are more spread out, so each m³ weighs less: the density falls from 1.32 kg/m³ at −10 °C to 1.11 kg/m³ at 40 °C. This is why warm air rises. The orange dot is our room: 1.17 kg/m³, which makes about 84 kg of air in the whole 72 m³.

## A2. The data table: how much water can air hold?

The sheet gives measured saturation pressures of water. Between table points we interpolate linearly (a straight line between neighbours). Error is under about 1 %, fine for this lab.

**What "100 % humidity" (saturation) means.** At a given temperature $t$, air can carry water vapour only up to a maximum vapour pressure, the **saturation pressure** $p_{sat}(t)$. The real vapour pressure in the air, $p_v$, is always at or below it. **Relative humidity** says how close the air is to that maximum:

- $\varphi$ = 100 % means $p_v=p_{sat}(t)$: the air is **full** (saturated) *at its current temperature*. One more drop of vapour would not stay a gas, it would condense (dew, fog, cloud). "100 % humidity", "100 % relative humidity" and "saturated air" are three names for this one state.
- 100 % does **not** mean "the air is made of water". The air still holds only a few grams of vapour per kg (see $x$ in A3); 100 % just means that, at this temperature, it cannot hold more.
- $\varphi$ = 60 % means the air carries 60 % of its maximum. $\varphi$ = 0 % is perfectly dry air.
- The black curve in the chart below is $p_{sat}(t)$, so **it is the set of all states with $\varphi$ = 100 %**. Every other relative humidity is a curve underneath it ($60\,\% = 0.60\cdot p_{sat}(t)$, the dashed line). A point *on* the curve is full air, a point *below* it can still take water, and a point *above* it cannot exist as vapour.
- The limit moves with temperature, so the same water gives different percentages: the sheet's summer air (30 °C, $p_v$ = 2548 Pa) is only 60 % full, but if it is cooled to 21.4 °C the same 2548 Pa reaches the curve and the air is 100 % full. That temperature is the **dew point** (A4).

![Saturation curve, relative humidity and dew point on one chart](figures/vapour-pressure-dew-point.svg)

*Figure: Saturation curve, relative humidity and dew point on one chart*

    
![png](figures/output_9_0.png)
    

**Reading it.** Follow the black curve from left to right: it bends upward, so from 0 °C to 30 °C the capacity grows about **7 times** (611 → 4247 Pa). That is why the same percentage means very different amounts of water on a summer and a winter day (A3). The orange arrow at 30 °C shows how much room the sheet's summer air still has and the horizontal arrow shows how far it must cool to close that gap.

## A3. Solving the sheet: summer day vs winter day

Both days: $p$ = 1 bar. Summer: $t$ = 30 °C, $\varphi$ = 60 %. Winter: $t$ = 0 °C, $\varphi$ = 85 %.

Steps for each day:

1. $p_{sat}(t)$ from the table.
2. $p_v = \varphi\cdot p_{sat}(t)$: the real water pressure.
3. $x = 0.622\,p_v/(p-p_v)$: grams of water per kg of dry air.
4. $t_{dp} = t_{sat}(p_v)$: look the value of $p_v$ up in the table **backwards** to get a temperature.
5. $h = t + x(2500 + 1.84\,t)$: energy per kg of dry air.

    
![png](figures/output_12_0.png)
    

**Reading the chart.**
- **Summer:** the air carries 16.3 g of water per kg of dry air. For comparison, the lecture gives 10 g/kg as the yearly average for Romania, and the comfort standard ASHRAE 55 (American Society of Heating, Refrigerating and Air-Conditioning Engineers, standard 55; used in Part B) caps the humidity ratio at 12 g/kg. Its dew point is 21.4 °C: any surface colder than that (a cold glass, an air-conditioner coil) will drip.
- **Winter:** only 3.2 g/kg. Dew point −2.2 °C: below that, frost or fog forms. Humidity of 85 % *sounds* wet, but cold air holds so little that the absolute amount of water is five times smaller than in summer.
- **Why the percentage misleads:** relative humidity compares $p_v$ with a limit that changes with temperature (A2), so it cannot be compared between a warm and a cold day. $x$ (and $p_v$) tell the real amount: warm air at 60 % holds much more than cold air at 85 %.

## Why do we use vapour *pressure* and not kilograms of water?

**Short answer: we use both, and they are the same information in two forms.** $p_v$ and $x$ are tied together by the ideal gas law, and the sheet uses each where it is the more convenient.

**The link.** Each gas in the mixture follows $pV = mRT$ on its own (Dalton's law). For the vapour and the dry air in the same volume $V$ and at the same temperature $T$:

with $R_a$ = 287 and $R_v$ = 461.5 J/(kg·K), so $R_a/R_v = 0.622$. Also, $p_v = \rho_v R_v T$: **the vapour pressure is just "kilograms of vapour per m³", multiplied by $R_vT$.** Pressure *is* a measure of quantity.

**Why pressure is the natural choice for these jobs:**
1. **Saturation is defined by pressure.** Water vapour can only reach a maximum partial pressure $p_{sat}(t)$ that depends (almost) only on temperature. So "is it full?" is the question $p_v \ge p_{sat}$, and relative humidity is just $\varphi = p_v/p_{sat}$. In kg you would need a different limit for every pressure and temperature.
2. **Dew point** is the temperature where $p_{sat}(t_{dp}) = p_v$, a single table look-up.
3. **Physical measurements** (hygrometers, the evaporation/condensation balance at a surface) respond to the vapour pressure.

**Why we *also* need the kg-based $x$:**
- $x$ is *conserved*: if you heat or cool air and add or remove no water, $x$ does not change. $p_v$ also stays put at constant total pressure, but the vapour **per m³** (and so $\varphi$) changes because the air expands. Mass balances, humidifying and dehumidifying, and enthalpy ($h$ is "per kg of dry air") all need $x$.
- $x$ is **directly** $m_v/m_a$, The code below shows both routes give the same number.

    vapour : 18.21 g per m3     dry air: 1.120 kg per m3
    x = rho_v/rho_a = 16.26 g/kg      formula 0.622*pv/(p-pv) = 16.26 g/kg   (same thing)
    

    
![png](figures/output_15_1.png)
    

**Reading it.** In the charts the humidity ratio $x$ and the vapour pressure $p_v$ **do not change** while we heat the air, since nothing was added or removed. But the vapour per m³ falls (air expands), and the relative humidity falls from 80 % (at 25 °C) to 35 % (at 40 °C), because the "full" limit $p_{sat}$ rises quickly. That is why *relative* humidity is a poor measure of the amount of water, while $x$ (kg/kg) and $p_v$ (Pa) tell the truth.

### Heating the air: where does the extra volume go, and why do $x$ and $t_{dp}$ stay put?

Two statements look contradictory:
1. *Warm air expands, so a cubic metre contains fewer molecules (less vapour, less dry air).*
2. *The humidity ratio $x$ and the dew point $t_{dp}$ do not change when we only heat the air.*

They do not contradict each other, because **$x$ and $t_{dp}$ never measure "how much per m³"**. $x$ compares the vapour with the dry air *that is in the same place*, and $t_{dp}$ is set by $p_v$, the share of the pressure that the vapour provides, which is the vapour's share of the molecules times the total pressure. Heating changes how many molecules fit in a cubic metre, not how they are mixed. What happens to the total pressure then depends on whether the extra volume has somewhere to go.

**A. A real room (it leaks, nothing is airtight).** The heated air tries to expand: at constant pressure $V\propto T$. The part that no longer fits in the room escapes through cracks, windows and ventilation, **taking vapour and dry air out in the same proportion as they were mixed**. The molecules that stay have the same mix, so $x$ is unchanged. The pressure stays at the outside value (1 bar), so $p_v=(\text{vapour share})\cdot p$ is unchanged and the dew point is unchanged. Per m³ there is less of both (the grey and blue dots in the figure inside the room are fewer), and the relative humidity falls because $p_{sat}$ grew (A2). The air did not go "somewhere else" in the sense of losing its water content: it just left with its own share of water.

**B. An isolated (sealed, rigid) room.** Nothing can leave and the volume cannot grow, so the same molecules now move faster and hit the walls harder. Pressure rises, and not magically: it is the ideal gas law $p=\rho R T$ with $\rho$ fixed, so $p\propto T$. From 30 °C to 40 °C that is a factor $313.15/303.15=1.033$, so 1 bar becomes about 1.033 bar (3.3 kPa more: this is why sealed cans and bottles burst when heated). Each gas's partial pressure rises by the same factor, so $p_v$ rises from 2548 to 2632 Pa. Since the masses of vapour and dry air did not change, **$x$ is exactly unchanged**, but because $p_v$ rose the **dew point rises slightly, from 21.4 °C to 21.9 °C**. So your intuition about a pressure increase is right for a sealed room, but the effect on the dew point is small (+0.55 °C), and it comes from the pressure increase, not from the expansion.

![Heating a sealed and a leaky room: what changes and what does not](figures/sealed-vs-leaky-room.svg)

*Figure: Heating a sealed and a leaky room: what changes and what does not*

    
![png](figures/output_19_0.png)
    

    
![png](figures/output_20_0.png)
    

## A4. Dew point on the saturation curve

Start at the air's state: its temperature and its $p_v$. Cool it **without adding or removing water**. Then $p_v$ does not change, so the state moves along a **horizontal line to the left**, while the temperature falls and the curve $p_{sat}(t)$ above it comes down to meet it. The meeting point is where the air reaches 100 % relative humidity (the saturation curve of A2): the **dew point**. Each day's own relative humidity ($60\,\%$ in summer, $85\,\%$ in winter) is the dashed curve through its starting point.

**The dew point as a function.** The dew point is the temperature at which the saturation pressure equals the air's vapour pressure:

So it is the **inverse of the saturation curve**: you enter with $p_v$ and read off a temperature. Sheet 1 does this by reading the table backwards (interpolating between rows). Sheet 2 gives the curve as the Antoine equation, $p_{sat}(t)=e^{16.6536-4030.183/(t+235)}$ in kPa, and solving it for $t$ gives a closed formula:

If only the air temperature $t$ and the relative humidity $\varphi$ are known, first get $p_v=\varphi\cdot p_{sat}(t)$ and then apply the formula.

**Why the dew point does not depend on the air temperature.** "Saturation pressure" means two different things here:
- the **curve** $p_{sat}(\cdot)$, a fixed property of water, the same for any air;
- the **value** $p_{sat}(t)$ at the air's current temperature, one point of that curve, which is the air's current ceiling.

The dew point uses the curve, read backwards from $p_v$, and never the air temperature $t$. When the air is heated and no water is added, the ceiling $p_{sat}(t)$ rises and the relative humidity falls, but $p_v$ and the curve are unchanged, so $t_{dp}$ is unchanged. The dew point moves only when $p_v$ moves: evaporation raises both, condensation lowers both, and in a sealed room heating raises $p_v$ slightly (see the section on heating the air above). Because $p_{sat}$ always increases with temperature, a higher dew point always means more water in the air.

![Cooling humid air to its dew point and below: when condensation starts](figures/humidity-ratio-and-dew-point.svg)

*Figure: Cooling humid air to its dew point and below: when condensation starts*

![A simplified psychrometric chart: humidity ratio against temperature](figures/psychrometric-chart.svg)

*Figure: A simplified psychrometric chart: humidity ratio against temperature*

    
![png](figures/output_24_0.png)
    

**Reading it.** Circle = the air now. Square = its dew point, always **on the black 100 % curve**. The arrow is the cooling path, a constant-$p_v$ line. Summer air only has to cool by about 8.6 °C before it reaches 100 % and fogs; winter air by about 2.2 °C, even though its relative humidity (85 %) looks closer to full than the summer's 60 %: the arrow is short because both the starting point and the curve are low (small $p_{sat}$).

## Condensation: what it is and when it happens

**Condensation** is water vapour turning into **liquid** water (the reverse of evaporation). It is what makes dew, fog, clouds, the mist on a bathroom mirror and the drops on a cold glass.

**When:** the air can only carry vapour up to $p_{sat}(t)$. If the air is cooled (or a cold surface touches it) so that $p_v$ would exceed $p_{sat}$, the excess cannot stay a gas and **becomes liquid**. The temperature at which this starts is exactly the **dew point** $t_{dp}$. So:

- surface warmer than $t_{dp}$ → stays dry;
- surface colder than $t_{dp}$ → the air next to it condenses on it.

**Energy:** condensing **releases** the latent heat that evaporation absorbed, about 2500 kJ per kg of water. An air-conditioner coil therefore does two jobs, cooling the air *and* making it condense (drying it), and the second one costs a lot of energy.

**Why buildings care:** a winter window or a cold wall corner below the room's dew point collects water, which leads to mould, damaged finishes and (when below 0 °C) frost.

**Two humidity ratios appear in the chart below, and they are different quantities.**
- **Actual humidity ratio $x$**: the water the air really carries. If no water is added or removed, it **does not change with temperature**, so on the chart it is a flat line.
- **Saturation humidity ratio $x_{sat}(t)$**: the humidity ratio the air would have if it were 100 % full at temperature $t$. It is the same formula as $x$ with $p_{sat}(t)$ in place of $p_v$:

It depends only on the temperature. It is the saturation pressure curve of A2 rewritten in g/kg: the **ceiling** for each temperature, not the amount of water that is there.

Cooling moves the air to the left along the flat line (nothing is removed, so $x$ is constant) until the line meets the ceiling: the dew point. Cooling further, the ceiling would drop below $x$, which is impossible, so the excess condenses and $x$ falls, following the curve. **$x$ changes with temperature only after condensation has started.**

    At 15 degC the air can hold only 10.81 g/kg, it carries 16.26 g/kg
    -> 5.45 g of every kg turns to liquid; for the room's 84.14 kg of air that is 459 g of water
    -> condensing releases 13.6 kJ per kg of air, 1146 kJ in the room
    

    
![png](figures/output_28_1.png)
    

**Reading it.** Summer air (30 °C, 60 %) has a dew point of 21.4 °C. Cooled to 15 °C it can hold only about 10.8 g/kg instead of 16.3, so about 5.5 g per kg of air turns to liquid. For the 84 kg of air in our room that is roughly **0.46 litres of water** and about **1.1 MJ** of latent heat released. In the chart, the green area is the "too much" water that has to leave the air. The flat orange line is the water the air really carries (constant while cooling), the blue curve is the ceiling $x_{sat}(t)$, and the two arrows mark the two stages: along the flat line down to the dew point, then along the curve while the excess condenses.

## Specific heat: how much energy does it take to warm something?

**Definition.** The **specific heat** $c$ of a substance is the energy needed to raise **1 kg** of it by **1 K** (1 °C):

"Specific" means "per kg". A large $c$ means the material is hard to warm up and stores a lot of heat (water); a small $c$ means it warms quickly (air). For gases it depends on whether the pressure is held fixed ($c_p$, used for open air at constant pressure) or the volume ($c_v$). We use $c_p$.

- **Dry air**: **1.006** (the sheet rounds it to 1, which changes $h$ by only 0.25 %)
- **Water vapour**: **1.84**
- **Liquid water**: **4.19**

**Where it appears in the sheet.** The enthalpy formula is just specific heats applied to the two ingredients:

The 1 in front of $t$ is the specific heat of dry air, and the 1.84 is the specific heat of water vapour. The 2500 kJ/kg is *not* a specific heat: it is the **latent heat of vaporisation**, the energy to turn 1 kg of liquid into vapour at 0 °C with no temperature change.

    
![png](figures/output_31_0.png)
    

![Specific heat: air versus water for the same mass and the same 1 K step](figures/specific-heat.svg)

*Figure: Specific heat: air versus water for the same mass and the same 1 K step*

    warm the room's air by 1 K :   84.6 kJ
    warm the same MASS of water:  352.5 kJ   (4.2 times more)
    h = 30.00 (dry air) + 0.90 (vapour warmth) + 40.66 (latent) = 71.56 kJ/kg
    with c_pa = 1.006 instead of 1: h = 71.74 kJ/kg (difference 0.25 %)
    

**Reading it.** To warm the room's air by 1 °C takes about 85 kJ, but the same mass of water would need over 350 kJ: water stores about 4 times more heat per kg than air. In the enthalpy of the summer air, 30 kJ/kg is the dry air's warmth, 0.9 is the vapour's warmth and 40.7 is the latent energy.

## A5. Enthalpy: where is the energy hiding?

$h = \underbrace{t}_{\text{sensible}} + \underbrace{x(2500+1.84\,t)}_{\text{latent}}$

- **Sensible** heat is the warmth you can feel and measure with a thermometer.
- **Latent** heat is energy stored in the water vapour (what it took to evaporate it). You do not feel it directly, but an air conditioner must remove it to dry the air.

![Enthalpy split into sensible and latent parts for 30 °C, 60 % air](figures/enthalpy.svg)

*Figure: Enthalpy split into sensible and latent parts for 30 °C, 60 % air*

    
![png](figures/output_37_0.png)
    

**Reading it.** In summer, about 42 of the 71.6 kJ/kg are latent, hidden in the humidity. Cooling this air to a comfortable temperature is only half the job: the air also has to be dried. In winter, the latent part (8.1) is the whole enthalpy, because 0 °C contributes no sensible energy.

## A6. Individual work: the whole day (Bucharest, Meteonorm data)

The sheet gives **24 hourly values** of $t$ and $\varphi$ for **August 8th** and **February 1st** (UTC = Coordinated Universal Time, the world reference clock; Romanian local time is UTC+3 in summer, UTC+2 in winter). We apply the same five steps to every hour.

    
![png](figures/output_41_0.png)
    

**Reading it.**
- **Top row:** the vertical double arrows measure the gap between the solid line (air) and the dashed line (dew point), which is how many degrees the air is from fog (100 % relative humidity). In summer the smallest gap is about 1.5 °C at 04:00 (relative humidity 91 %) and the largest 13.4 °C at 16:00 (44 %). In winter the gap stays between 2.0 and 5.9 °C all day.
- **Bottom row:** the rings mark the highest and lowest humidity ratio. In summer the orange area is above 12 g/kg, the limit of the ASHRAE 55 comfort standard (the standard used in Part B and named in the lecture), from 01:00 to 09:00 UTC (13.4 to 14.8 g/kg until 08:00, only just above at 09:00) and again at 17:00. Even in the afternoon, when relative humidity is lowest, the air still holds 10 to 12 g/kg, so it is dry only in relative terms. Winter air never exceeds 4.8 g/kg, which is why heated winter rooms often feel too dry.

    
![png](figures/output_43_0.png)
    

**Reading it.** This is the classic *psychrometric chart*: temperature across, water content up. Each dot is one hour. The black curve is the **100 % relative humidity** (saturation) curve of A2, drawn here in terms of $x$: no hour can lie above it, because that air would already be fog. The grey curves under it are 80, 60, 40 and 20 %: a dot between two curves has the percentage in between.
- **Summer night** (01:00 to 08:00, dashed oval on the left): 80 to 91 %, just under the black curve, so the air is almost fog.
- **Summer afternoon** (12:00 to 16:00, oval on the right): 44 to 53 %, far below the curve. The dashed arrow shows the day moving from the night oval to the afternoon oval: the air warms and the dots slide away from the 100 % curve.
- **Winter** (blue oval): bottom left, 66 to 87 %, but it holds so little water that it is far below the summer cloud.

Air conditioning moves summer dots **down** (drying) and **left** (cooling) toward the comfort zone.

    
![png](figures/output_45_0.png)
    

    Summer: h from 40.8 to 60.4 kJ/kg;  winter: 9.9 to 19.5 kJ/kg
    

**Reading it.** The two-headed arrow on the right compares the daily averages: summer air carries roughly three times as much energy per kg as winter air (41 to 60 kJ/kg against 10 to 20). The rings mark each curve's highest and lowest hour. The summer peak is at 08:00, not in the hot afternoon, because that is when the air is still very humid (14.6 g/kg) and already warm (A7 explains this link). An air-handling unit's workload follows these curves: the higher $h$, the more energy it needs to bring the air to indoor conditions.

## A7. Reading the curves: what moves when something else moves

The charts above show a handful of quantities, and they are **computed from each other** with the formulas of A3: only the air temperature $t$ and the relative humidity $\varphi$ are measured, and everything else follows. This section uses the 24 hourly values of both days to show **which curves rise and fall together, which are mirror images, and why**, with the pattern marked on each figure.

**How to read a correlation.** The correlation $r$ between two curves is a number from −1 to +1. Hour by hour it asks: when curve A is above its own average, is curve B above its average too?

- $r$ close to **+1**: they rise and fall together (left plot, orange arrow slopes up);
- $r$ near **0**: no relation, the dots form a cloud (middle plot);
- $r$ close to **−1**: mirror images, when one rises the other falls (right plot, arrow slopes down).

    
![png](figures/output_48_0.png)
    

    
![png](figures/output_48_1.png)
    

**Map of the links.** Every arrow means "is computed from". 
1. **Water amount.** $\varphi$ and $t$ give $p_v$, and then both $x$ and $t_{dp}$ come from $p_v$ alone. So $x$ and $t_{dp}$ are *the same information* in g/kg and in °C: their curves must have the same shape (section 3).
2. **Relative humidity.** $\varphi=p_v/p_{sat}(t)$ uses $t$ again, through the growing $p_{sat}(t)$. If $t$ goes up and the water stays the same, $\varphi$ must go down (section 2). The gap $t-t_{dp}$ measures the same thing in degrees (section 4).
3. **Energy.** $h$ takes $t$ as its sensible part and $x$ as its latent part, so it follows whichever of the two changes more over the day (section 5).

    
![png](figures/output_50_0.png)
    

### 2. Temperature and relative humidity: mirror images

If the air warms and gains no water, $p_v$ stays the same but $p_{sat}(t)$ grows (A2), so $\varphi=p_v/p_{sat}$ falls. Over a day the temperature rises from the morning minimum to the afternoon peak, so relative humidity should fall in the same hours.

In the figure the coloured line is $t$ (left axis) and the dashed black line is $\varphi$ (right axis). The wide translucent arrows cover the morning-to-afternoon stretch: **$t$ climbs while $\varphi$ drops**. The rings mark the extreme hours and the dotted vertical line the hour of the lowest $\varphi$.
- **Summer** ($r=-0.75$): $t$ climbs from 20.7 °C (05:00) to 27.9 °C (15:00) while $\varphi$ drops from 89 % to 46 %. $\varphi$ is lowest (44 %) at 16:00, one hour after the temperature peak, and highest (91 %) at 04:00, when $t$ is only 21 °C. The mirror is not perfect because the water in the air also changes: at 17:00 $\varphi$ jumps from 44 % to 56 % while $t$ falls only 0.6 °C.
- **Winter** ($r=-0.89$): $t$ climbs from 1.1 °C (07:00) to 7.9 °C (13:00) while $\varphi$ drops from 85 % to 69 %. The swing is smaller (66 to 87 % all day) because the winter air also gains water as it warms (section 3), which partly refills the bigger $p_{sat}$.

    
![png](figures/output_52_0.png)
    

### 3. Dew point and humidity ratio: the same curve

$t_{dp}$ is $p_v$ read backwards in the saturation table, and $x=0.622\,p_v/(p-p_v)$. Both are functions of $p_v$ alone, so they are one quantity written in °C and in g/kg.

In the first two panels the dashed line ($x$, right axis) lies on top of the solid line ($t_{dp}$, left axis); the two axes are scaled so the shapes can overlay. The dotted vertical lines and rings mark the hours of the highest and the lowest value: **both curves peak and bottom out in the same hour**, $r=1.00$.
- **Summer:** both highest at 02:00 ($t_{dp}$ 19.9 °C, $x$ 14.8 g/kg), both lowest at 24:00 (11.3 °C, 8.5 g/kg).
- **Winter:** both highest at 12:00 (3.1 °C, 4.8 g/kg), both lowest at 06:00 (−1.3 °C, 3.5 g/kg).

The right panel plots $x$ against $t_{dp}$. All 48 hours fall on **one curve, the saturation curve of A2** (the 100 % line) written as $x_{sat}$ at the temperature $t_{dp}$. This is the definition of the dew point: air with humidity ratio $x$ is 100 % full exactly at the temperature where $x$ meets the saturation curve. The summer ring sits high on the curve (humid, high dew point), the winter ring low on it (dry, low dew point).

    
![png](figures/output_54_0.png)
    

### 4. The gap $t-t_{dp}$ and relative humidity

The gap is how many degrees the air must cool before it reaches 100 % relative humidity (A4). So the smaller the gap, the fuller the air: at **gap = 0 the relative humidity is exactly 100 %** (the star on the figure). The points fall along a line sloping down from the star, $r=-1.00$ on both days: the larger the gap, the drier the air.

The dashed ovals show where the hours sit:
- **Summer night** (01:00 to 08:00): gap 1.5 to 3.6 °C and $\varphi$ 80 to 91 %, close to the star, so the air is almost fog.
- **Summer afternoon** (12:00 to 16:00): gap 10.4 to 13.4 °C and $\varphi$ 44 to 53 %, the dry end of the line.
- **Winter** (all hours): gap 2.0 to 5.9 °C and $\varphi$ 66 to 87 %, never far from fog, even though the absolute water content is small.

    
![png](figures/output_56_0.png)
    

### 5. Enthalpy: does it follow the temperature or the water?

$h=t+x\,(2500+1.84\,t)$ is a sensible part ($t$) plus a latent part (proportional to $x$), so $h$ follows whichever varies more over the day. Each panel plots $h$ against one of them; the wide stripe is the trend line and the label says whether it is a tight line or a loose cloud.
- **Winter** ($r(t,h)=0.99$, $r(x,h)=0.96$): $t$ and $x$ rise together ($r(t,x)=0.93$), so $h$ follows both and both panels are tight lines. The sensible part swings by 6.8 kJ/kg (1.1 to 7.9 °C) and the latent part by only 3.3 kJ/kg (8.7 to 12.0), so temperature leads.
- **Summer** ($r(t,h)=0.33$, $r(x,h)=0.84$): here $t$ and $x$ are almost unrelated ($r=-0.23$): the humid hours are the cool night hours. The latent part swings by 16.1 kJ/kg (21.5 to 37.6) and the sensible part by 8.6 kJ/kg (19.3 to 27.9 °C), so the water leads. The temperature panel is a loose cloud, the water panel a much tighter line.
- **The rings in the summer panels** mark two hours. At 08:00 the temperature is only 23.3 °C, yet $h$ is the day's highest (60.4 kJ/kg) because $x$ is 14.6 g/kg. At 24:00 it is the coolest and driest hour, with the lowest $h$ (40.8 kJ/kg).

    
![png](figures/output_58_0.png)
    

# Part B: Sheet 2, the comfort challenge (PMV, PPD, $t_o$)

Sheet 1 described the air. Now we look at the **person in the air**.

### What do PMV and PPD stand for, and where do they come from?

**PMV = Predicted Mean Vote.** In the 1960s the Danish professor P. O. Fanger put volunteers in climate chambers, changed the air temperature, humidity, air speed, clothing and activity, and asked them to **vote** on how they felt on the **7-point thermal sensation scale** (the ASHRAE scale): −3 cold, −2 cool, −1 slightly cool, 0 neutral, +1 slightly warm, +2 warm, +3 hot. He published the method in his book *Thermal Comfort* (1970).
- **Vote**: one person's answer on that 7-point scale.
- **Mean**: the average vote of a large group of people in the same room.
- **Predicted**: nobody is asked. The number is *calculated* from the six inputs ($t_a$, $t_{mr}$, $v$, relative humidity, clothing, activity) with the heat balance of the body: heat produced minus heat lost is the thermal load $L$, and $PMV=TS\cdot L$. If heat piles up ($L>0$) people vote warm, if the body loses heat faster than it makes it ($L<0$) they vote cool.

**PPD = Predicted Percentage of Dissatisfied.** People differ, so even in a room that is right for the average person some are unhappy. PPD is the percentage of a large group who would be *dissatisfied*, which means they would vote **warm or hot (+2, +3) or cool or cold (−2, −3)**. Fanger fitted this curve to the votes: $PPD = 100-95\,e^{-0.03353\,PMV^4-0.2179\,PMV^2}$. It is smallest (5 %) at $PMV=0$ and grows quickly on both sides.

**ISO 7730** (ISO = International Organization for Standardization) is the international standard that fixes how to calculate PMV and PPD, including the iteration of Step 3. **ASHRAE 55** (ASHRAE = American Society of Heating, Refrigerating and Air-Conditioning Engineers; standard 55, *Thermal Environmental Conditions for Human Occupancy*) uses the same model to define comfort zones.

## B0. The big picture: six factors, six drains

The lecture says thermal comfort is a **heat balance** between body and environment, controlled by **four environmental** and **two personal** factors:

- **air temperature $t_a$, mean radiant temperature $t_{mr}$, air speed $v$, humidity RH**: metabolic rate $M_{met}$, clothing $I_{clo}$

The body makes heat $M$. Six paths remove it ($RL_1$ to $RL_6$). What remains is the load $L$, and $PMV = TS\cdot L$.

Which factor drives which drain? The heatmap below changes each factor by one typical step and shows how many W/m² each drain moves by (orange = drain grows, blue = shrinks). The hot summer day is the base case.

![The six factors that PMV combines](figures/pmv-six-factors.svg)

*Figure: The six factors that PMV combines*

![How the body gives heat to its surroundings](figures/body-heat-exchange.svg)

*Figure: How the body gives heat to its surroundings*

    
![png](figures/output_62_0.png)
    

**Reading it.** Each column is a factor, each row a drain.
- **Humidity** acts only on the two vapour drains ($RL_1$, $RL_3$): it is the $p_v$ of sheet 1. More humid air means *less* vapour loss (blue).
- **Metabolic rate** mostly adds **sweat** ($RL_2$, +2.4 W/m² per 0.1 met). The other drains change slightly, because a busier body has a cooler skin and clothing.
- **Air speed** acts on convection ($RL_6$, +2.3 W/m² per 0.1 m/s). Radiation drops a little because the clothes get cooler.
- **$t_a$ and $t_{mr}$ push in opposite directions on the two big drains:** warmer air shrinks convection loss (−4.0), warmer walls shrink radiation loss (−3.9), while the other drain rises slightly. In both cases total heat loss falls and PMV rises.
- **Clothing** reduces both radiation and convection (about −0.7 each per 0.1 clo): it is the insulation.

## B1. Metabolic rate in depth (lecture slides 16 to 20)

A resting adult produces about **100 W** of heat. Spread over the skin (about 1.7 m² on average; 1.8 m² for a European man, 1.6 m² for a woman) this is about 58 W/m², which is what defines **1 met**. The lab uses the exact value 58.15 W/m². The lecture also gives two helpful formulas.

**Skin temperature** falls as activity rises (more sweat cools the skin): $t_{sk} = 35.7 - 0.0275\,(M - W)$, with $W$ the mechanical work done (zero for desk work). The lab's clothing-balance equation uses $35.7 - 0.028\,M$, the same idea rounded.

**Measuring M from breathing** (Nishi 1981): $M = 21\,(0.23\,RQ+0.77)\,\dfrac{\dot V_{O_2}}{A_D}$, where $RQ$ is the *respiratory quotient* (CO₂ out / O₂ in; it tells which fuel the body burns: about 0.7 for fats, 1.0 for carbohydrates, about 0.83 for a mixed diet), $\dot V_{O_2}$ is oxygen consumption (mL/s) and $A_D$ is skin area (m²).

![Typical values of clothing insulation (clo) and metabolic rate (met)](figures/clothing-and-activity.svg)

*Figure: Typical values of clothing insulation (clo) and metabolic rate (met)*

    
![png](figures/output_66_0.png)
    

**Reading it.** The skin temperature drops about 1 °C between resting and 1.5 met, which is why $t_{cl}$ depends on $M$ in the iteration. Above about 3 met the activity is poorly defined and the values can be off by ±50 %, so PMV is a less reliable number there.

## B2. Clothing in depth

- **clo** is the unit of clothing insulation. **1 clo = 0.155 m²·K/W**: the thermal resistance of a typical winter business suit. 0.5 clo is light summer clothing.
- Clothes also **enlarge the surface** that exchanges heat. The *clothing area factor* $f_{cl}$ = clothed surface / nude surface:

    
![png](figures/output_69_0.png)
    

**Reading it.** At 0.5 clo the insulation is just under the 0.078 threshold, so the **first** branch applies (it differs only slightly from the second). The area factor is about 1.10: a lightly dressed body exchanges heat over a surface 10 % larger than bare skin.

## B3. Mean radiant temperature and operative temperature, properly

**Mean radiant temperature** $t_{mr}$ is the average temperature of everything the body "sees", weighted by how much of the body faces each surface. The lecture gives weights for a **seated** person (up/down, right/left, front/back):

(standing: 0.08, 0.23, 0.35). In the lab we are simply **given** $t_{mr}$ = 30.5 °C.

![Cold surfaces: why operative temperature, not only air temperature, matters](figures/radiant-cold-window.svg)

*Figure: Cold surfaces: why operative temperature, not only air temperature, matters*

**Operative temperature.** The lecture's physical definition is a weighted average with the two heat-transfer coefficients as weights:

with $h_c$ convective and $h_r$ radiative coefficient [W/(m²·K)], $\varepsilon$ emissivity (assumed 0.95 here), $\sigma = 5.67\cdot10^{-8}$ W/(m²K⁴), $A_r/A_D$ = 0.70 sitting or 0.73 standing.

The **sheet simplifies this to fixed weights** (0.5/0.5, 0.6/0.4, 0.7/0.3 depending on air speed). Let us check that the simplification is reasonable.

    
![png](figures/output_74_0.png)
    

**Reading it.** The physical curve rises with air speed (more convection, so air counts more), just like the sheet's steps. At the lab's 0.15 m/s the physical weight is about 0.52 against the sheet's 0.50, so the two operative temperatures (30.24 and 30.25 °C) are practically identical. The sheet's version needs no iteration and no emissivity, which makes it easy to code and good enough for control.

## B4. The heart of the code: the $t_{cl}$ iteration (what the sheet calls Step 3)

Why iterate? $t_{cl}$ sets how much heat leaves by radiation ($\propto T_{cl}^4$) and convection ($h_c$ depends on $t_{cl}-t_a$), and those losses in turn set $t_{cl}$. The sheet's recipe is *guess, recompute, repeat until the change is below $\epsilon=0.0015$*.

**Why our numbers match the sheet exactly.** The reference result (PMV 1.767, 8 iterations) only appears with this ISO 7730 form: kelvin = °C + 273.15, the balance constant 308.7 (=35.7 + 273), unknown $x=T_{cl}/100$, old/new values averaged each round, and the stopping test applied to $x$ (so 0.0015 means 0.15 K). A looser or different choice gives PMV 1.71 to 1.76, which is close but does not match the sheet.

![The t_cl iteration: guess, correct, repeat until the change is below the stop band](figures/tcl-iteration.svg)

*Figure: The t_cl iteration: guess, correct, repeat until the change is below the stop band*

    
![png](figures/output_78_0.png)
    

    -> t_cl = 32.10 degC after 8 iterations;  h_c = 4.69 W/m2K;  f_cl = 1.10
    

## B5. Reading PMV and PPD like a standard (lecture slides 28 to 30)

- **PMV scale:** +3 hot, +2 warm, +1 slightly warm, 0 neutral, −1 slightly cool, −2 cool, −3 cold.
- **Even at PMV = 0, at least 5 % of people are dissatisfied.**
- **Validity:** the model assumes sweating is small, so PMV is only applicable for $-2 < PMV < +2$. It is **not applicable for hot environments**.
- **Romanian regulation I5 (the national normative that defines the comfort categories, as named in the lecture)** sorts rooms into four categories:

- **I high**: children, elderly, sick — < 6 % — −0.2 … 0.2
- **II medium**: normal for new / renovated buildings — < 10 % — −0.5 … 0.5
- **III moderate**: existing buildings — < 15 % — −0.7 … 0.7
- **IV low**: short periods only — > 15 % — beyond ±0.7

The lab's target, −0.5 < PMV < 0.5, is category **II**.

![The PMV scale from cold to hot and the comfort categories](figures/pmv-scale.svg)

*Figure: The PMV scale from cold to hot and the comfort categories*

    
![png](figures/output_81_0.png)
    

**Reading it.** Our indoor room (PMV −0.03) sits in the centre, **category I**, the strictest one (|PMV| < 0.2, PPD 5.0 % < 6 %). The outdoor day (+1.77) is in category IV, and its value is just inside the ±2 validity limit, so the number can be trusted but is close to the edge.

## B6. Applying the comfort model to the whole summer day

The challenge refers to *"the considered day in the previous simulation"*. Here we run the hourly summer data of sheet 1 through the comfort program, assuming (as the sheet does for its single case) $t_{mr}=t_a+0.5$ °C, $v=0.15$ m/s, 0.5 clo, 1.2 met. **This is an extension, not something the sheet asks for**: it shows how the outdoor air would feel to a person dressed for summer.

    
![png](figures/output_84_0.png)
    

    PMV from -1.66 (hour 24) to 0.96 (hour 15)
    

**Reading it.** The air is **cool** at night and in the early morning (PMV down to −1.66 at the last hour, 19.3 °C), comfortable around 08:00 to 11:00 and again 18:00 to 21:00 UTC, and **warm** from noon to evening (peak +0.96 at 15:00 UTC, 27.9 °C and 46 %). The sheet's example state (30 °C, 60 %) is hotter and more humid than any hour of this particular day, which is why its PMV (+1.77) is higher than this day's peak.

## B7. Finding the indoor conditions (the second half of the challenge)

The sheet fixes RH, $v$, clothing and activity, and lets us change $t_a$, $t_{mr}$ (and RH). **Summer rule: $t_{mr}=t_a+0.5$.** We search for the $t_a$ range where $-0.5<PMV<0.5$, and compare with the ASHRAE 55 operative-temperature ranges from the lecture: **23 to 26 °C in summer (0.5 clo), 20 to 24 °C in winter (1.0 clo)**.

    Summer clothes (0.5 clo, 1.2 met): -0.5 < PMV < 0.5 for t_a from 23.01 to 26.14 degC  (t_o 23.26 to 26.39)
    Winter clothes (1.0 clo, 1.2 met): -0.5 < PMV < 0.5 for t_a from 19.16 to 23.51 degC  (t_o 19.41 to 23.76)
    

    
![png](figures/output_87_1.png)
    

**Reading it.** Light bars = the ASHRAE 55 ranges from the lecture. Solid bars = what our PMV program says (PMV between ±0.5). They overlap well: the program reproduces the standard's comfort zone. Winter people wear twice the clothing, so the comfortable air temperature is lower.

## B8. Why the comfortable temperature depends on activity

Lecture slide 24: for activity above 70 W/m² the comfortable operative temperature **drops**, because the body makes more heat. Our program shows the same effect (summer clothes, $t_{mr}=t_a+0.5$):

    
![png](figures/output_90_0.png)
    

**Reading it.** Every extra 0.2 met lowers the comfortable air temperature by about 1.3 °C (the range is 24.6 to 27.1 °C at 1.0 met and 16.8 to 22.0 °C at 2.0 met). So a room that is perfect for a seated student feels hot to someone doing a lab practical on their feet.

## B9. Summary

- **Mass / density of air in 6×4×3 m room at 25 °C** (sheet 1): 84.14 kg, 1.17 kg/m³ (slide: 1.16)
- **Summer 30 °C, 60 %: $p_{sat}$, $p_v$, $x$, $t_{dp}$, $h$** (sheet 1): 4247 Pa, 2548 Pa, 16.26 g/kg, 21.4 °C, 71.6 kJ/kg
- **Winter 0 °C, 85 %: same** (sheet 1): 611.2 Pa, 519.5 Pa, 3.25 g/kg, −2.2 °C, 8.1 kJ/kg
- **Outdoor comfort (30 / 30.5 °C, 60 %)** (sheet 2): PMV 1.767, PPD 65.3 %, $t_o$ 30.25 °C, 8 iterations
- **Indoor comfort (24.5 / 25 °C, 60 %)** (sheet 2): PMV −0.027, PPD 5.0 %, $t_o$ 24.75 °C, 8 iterations (category I)

    Outdoor:  PMV= 1.767   PPD= 65.3 %   t_o= 30.25 degC   n iterations= 8
    Indoor:  PMV= -0.027   PPD= 5.0 %   t_o= 24.75 degC   n iterations= 8
