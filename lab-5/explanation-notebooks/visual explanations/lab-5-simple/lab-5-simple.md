# Lab 5 explained simply: which sun-heating panel wins?

**Lab 5: solar to thermal energy conversion.** A panel on the roof turns sunlight into hot water. We check how much heat one square metre delivers and why the weather decides which panel is better.

# Part 0: How a sun-heating panel works

A **solar thermal collector** is a panel that catches sunlight and uses it to warm up a liquid. Think of a black garden hose lying in the sun: the water inside gets hot. The panel does the same, but in a smart box that keeps the heat in.

> **Solar thermal collector**: a panel that turns sunlight into heat (not electricity) and hands that heat to a liquid.

The most common type is the **flat-plate collector**, a flat insulated box with a glass lid.

> **Flat-plate collector**: a flat box with a glass lid, a dark metal plate inside and pipes under the plate. The sun heats the plate, the plate heats the liquid in the pipes.

> **Absorber plate**: the dark metal plate inside the box that soaks up the sunlight, like a black T-shirt in summer.

> **Working fluid**: the liquid (water or water with antifreeze) that flows through the pipes and carries the heat away.

> **Glazing**: the glass lid. It lets sunlight in and slows the heat down on its way out, like a greenhouse roof. A **double-glazed** collector has two glass sheets, a **single-glazed** one has one.

> **Selective coating**: a special thin layer on the plate that swallows sunlight very well but gives off very little heat of its own. It is like a coat that is warm but does not let the warmth leak.

> **Insulation**: foam or mineral wool behind and around the plate, so the heat does not escape out of the back.

> **Irradiance** $G_T$ (W/m²): how much sunlight power lands on one square metre of the glass. A bright summer noon is about 1000 W/m², a grey winter day well below 300. Watts per square metre means "power for each square metre".

> **Inlet temperature** $T_i$ (°C): the temperature of the liquid when it enters the collector, set by what the liquid has just come from (a warm tank, for example).

> **Outside air temperature** $T_a$ (°C): the temperature of the air around the collector, called the "ambient" temperature. The collector loses heat to it.

> **Useful power** $q_u$ (W/m²): the heat that really ends up in the liquid, for each square metre of collector. It is what we want to know.

![A flat-plate collector from the side: sunlight comes in, some heat escapes through the glass, the rest warms the fluid](figures/collector-cross-section.svg)

*Figure: A flat-plate collector from the side: sunlight comes in, some heat escapes through the glass, the rest warms the fluid*

# Part 1: Efficiency and the characteristic curve

Not all the sunlight becomes useful heat. Some bounces off, some leaks away from the hot plate into the cold air. The share that is left is the **efficiency**.

> **Efficiency** $\eta$ (no unit, 0 to 1 or as a percentage): the share of the sunlight on the glass that becomes useful heat in the liquid. With $\eta = 0.5$, half of the sunlight is used. A collector's efficiency changes with the weather.

How good a collector is on a perfect day and how badly it suffers in the cold are two separate things, and each gets its own number:

> **Intercept** $F_R(\tau\alpha)$ (no unit): the efficiency when the liquid is as cold as the air, so nothing leaks. It tells how well the glass lets the light in ($\tau$, the share of sunlight the glass lets through) and how well the plate soaks it up ($\alpha$, the share of that light the plate absorbs). $F_R$ is a correction because the liquid warms up a little on its way. A bigger intercept is a better collector on a perfect day.

> **Slope** $F_R U_L$ (W/(m² K)): how fast the efficiency falls when the liquid gets hotter than the air. $U_L$ is the **loss coefficient**: the watts that leak out of the collector per square metre for each degree it is warmer than the air. A small slope is a well-insulated collector.

> **Reduced temperature** $x$ (K·m²/W): a single number for how hard the weather is on the collector: $x = (T_i - T_a)/G_T$. It grows when the liquid is much hotter than the air, or when the sun is weak. A difference of 1 °C equals a difference of 1 K, so degrees Celsius can be used directly.

With these, the efficiency is a **straight line**, the *characteristic curve*:

> **Characteristic curve**: the straight line $\eta = F_R(\tau\alpha) - F_R U_L\,x$. It starts at the intercept when $x = 0$ and goes down with the slope as $x$ grows. The useful power is then $q_u = \eta \cdot G_T$.

In words: *useful power = sunlight × (best possible share − losses)*.

![Where the sunlight goes: the intercept is what the plate absorbs, the slope term is what leaks away](figures/sun-to-heat-balance.svg)

*Figure: Where the sunlight goes: the intercept is what the plate absorbs, the slope term is what leaks away*

![Reading a characteristic curve: two lines with different intercept and slope, and where they cross](figures/efficiency-line-anatomy.svg)

*Figure: Reading a characteristic curve: two lines with different intercept and slope, and where they cross*

Data from the sheet: the double-glazed collector with a selective coating has an intercept of **0.70** and a slope of **3.5 W/(m² K)**. It runs on a winter afternoon with **600 W/m²** of sunlight, outside air at **5 °C** and liquid entering at **50 °C**.

# Q(a), Q(b), Q(c): the double-glazed collector on a winter afternoon

**Idea.** Work out how hard the weather is on the collector ($x$), read the efficiency from the line, then multiply by the sunlight.

    (a) x = 0.0750 K m2/W
    (b) eta = 0.4375  (43.7%)
    (c) q_u = 262.5 W/m2   (absorbed 420.0 - lost 157.5)
    

    
![png](figures/output_9_1.png)
    

**What this means.**
* **(a) x = 0.075 K·m²/W.** The liquid is 45 degrees hotter than the air and the sun is moderate, so the weather is fairly hard on the collector.
* **(b) Efficiency η = 0.4375, about 44 %.** Of 100 units of sunlight, 70 are absorbed at best, but the loss term takes 26 back, so 44 end up as heat.
* **(c) Useful power q_u = 262.5 W/m².** A 4 m² roof panel would deliver roughly 1 kW, about one electric kettle running all the time.
* In the bar above: of 600 W/m², 180 never get into the plate (reflection and glass), 157.5 leak away to the cold air and 262.5 warm the liquid. The leaking part is more than a third of what the plate absorbed, so the slope matters a lot in winter.

# Q(d): the double-glazed collector against the single-glazed one, each on its own day

**Idea.** The sheet gives the single-glazed collector a milder day: 750 W/m² of sunlight, air at 20 °C, liquid in at 45 °C, and a useful power of 412 W/m². Its extension gives its numbers: intercept **0.75** and slope **6.0 W/(m² K)**. They confirm the 412: the line gives η = 0.55 and 0.55 × 750 = 412.5 W/m².

    single-glazed on its own day: x = 0.0333, eta = 0.5500, q_u = 412.5 W/m2 (sheet: 412, eta from sheet = 0.5493)
    double-glazed on its own day: x = 0.0750, eta = 0.4375, q_u = 262.5 W/m2
    double-glazed placed on the single-glazed day: eta = 0.5833, q_u = 437.5 W/m2
    share of the absorbed sunlight lost: single 26.7%, double 37.5%
    

    
![png](figures/output_12_1.png)
    

**What this means.**
* **The single-glazed collector wins on its own day: 412 W/m² against 262.5 W/m²**, an efficiency of 55 % against 44 %.
* **Why, in physical terms.** On the mild day $x$ is small (0.033), so the leak term is only 6.0 × 0.033 = 0.20, about 27 % of what the plate absorbs. The collector's **intercept** does the work: its 0.75 is higher than the double-glazed 0.70. In the cold winter day $x$ is more than twice as big (0.075), so the double-glazed collector loses 37.5 % of what its plate absorbs. There its **slope** is what keeps it going: a slope of 3.5 instead of 6.0 saves a lot.
* **Careful: the weather, not the collector, won this round.** Put the double-glazed collector on the single-glazed collector's mild day and it would give η = 0.583 and **437.5 W/m²**, more than the 412. The single-glazed collector only "wins" because its day is far easier. A fair match needs the same weather, which is the next question.

# Q(e): both collectors on the same winter afternoon

**Idea.** Same sun, same air, same liquid temperature: 600 W/m², 5 °C and 50 °C, so $x = 0.075$ for both.

    winter day (G_T=600, T_i=50, T_a=5):  double eta = 0.4375, q_u = 262.5 W/m2;  single eta = 0.3000, q_u = 180.0 W/m2
    better: double-glazed, selective coating, by a factor 1.46
    

    
![png](figures/output_15_1.png)
    

**What this means.**
* **The double-glazed collector is better, by a factor of 1.46:** 262.5 W/m² against 180 W/m², or 44 % against 30 % efficiency.
* The single-glazed collector has the higher intercept (0.75), but its steep slope (6.0) takes 0.45 away at x = 0.075, leaving only 0.30. The double-glazed collector loses 0.2625 and keeps 0.4375.
* **The intercept alone would give the wrong answer.** Always look at the actual operating point.

# Q(f): where do the two lines cross?

**Idea.** At the crossing the two collectors are equally efficient. Set the two lines equal and solve for $x$.

> **Crossing point**: the value of $x$ where the efficiencies of two collectors are equal. On one side one collector is better, on the other side the other.

    crossing at x = 0.0200 K m2/W, where both have eta = 0.630
    below it: single-glazed; above it: double-glazed, selective coating
    G_T =  600 W/m2: crossing at a fluid-to-air difference of 12.0 K
    G_T =  750 W/m2: crossing at a fluid-to-air difference of 15.0 K
    G_T = 1000 W/m2: crossing at a fluid-to-air difference of 20.0 K
    

    
![png](figures/output_18_1.png)
    

**What this means.**
* **The lines cross at x = 0.02 K·m²/W**, where both collectors have an efficiency of 0.63.
* **Below x = 0.02 the single-glazed collector is better** (the intercept wins when losses are small). **Above it the double-glazed collector is better** (the slope wins when losses are big).
* In everyday terms: at 600 W/m² the crossing is at a difference of only **12 K** between liquid and air, at 750 W/m² at 15 K. A collector that heats a swimming pool, a few degrees above the air, belongs to the single-glazed side. A collector that heats a house in winter, 45 K above the air, belongs to the double-glazed side.
* All the cases of this lab sit above the crossing (x = 0.075 and x = 0.033), so in a fair comparison the double-glazed collector would win in both.

# Summary

* **(a)** x = 0.075 K·m²/W. **(b)** η = 0.4375. **(c)** q_u = 262.5 W/m².
* **(d)** On its own day the single-glazed collector gives more (412 W/m²) because its day is mild and its intercept does the work. On a cold day the slope matters and the double-glazed collector keeps more of the sun.
* **(e)** On the same winter afternoon the double-glazed collector gives 262.5 W/m² against 180 W/m².
* **(f)** The lines cross at x = 0.02 K·m²/W: below it the single-glazed collector is better, above it the double-glazed one.
* **Never judge two collectors by the intercept alone: check the actual operating point.**
