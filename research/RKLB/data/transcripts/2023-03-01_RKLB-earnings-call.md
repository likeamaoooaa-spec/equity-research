---
ticker: RKLB
quarter: Q3
year: 2023
source: https://roic.ai/quote/RKLB/transcripts/2023-year/3-quarter
downloaded: 2026-07-14
---



Peter Beck

Thanks, Colin and welcome everybody for joining us.Today’s presentation we will go over our key business accomplishments for the third quarter of 2023 as well as further achievements we have made since the end of the quarter.

Adam will then talk through our financial results for the third quarter before covering the financial outlook for Q4 2023.After that, we will take questions and finish today’s call with the near-term conferences we will be attending.

Alright.On to what we achieved – excuse me, in the third quarter for the year.

Starting with Electron, in July, we launched a mission with several satellites for NASA and others, which was the first of the two back-to-back reusability focused missions.After successfully deploying the first Mission 7 spacecraft, Electron’s first stage was bought back to Earth and recovered from the ocean.

Then we followed that up with our 40th Electron launch and even more recovery milestones, including a return for stage and thea first launch, reflowing Rutherford engine previously flown on our 26 Mission, There and Back Again.The engine performed flawlessly like a new one, completely validating our pursuit of reusability for Electron and setting us up well to refly an entire engine set as our next major reusability goal.

Next, I will provide a bit of an update for Electron.Following those two successful flights, as you know, we unfortunately experienced an anomaly on our 41st Mission.

It’s important to remember that up until this launch, we have had 37 successful orbital missions to place 171 satellites in orbit.And the past two years have been flawless, with a record of 20 successful missions one after the other.

For Flight 41, as soon as the issue occurred, a team jumped into action in the week since the team has been scarring through thousands of channels of flight data and manufacturing data to determine what was the probable root cause.I will take you through their investigation in detail over the next couple of slides.

Working in parallel with the FAA.The FAA has conducted its own review of the mission safety processes, plans and procedures, which concluded that they all worked as they should to keep the public safe and I am pleased to confirm that the FAA has since given us approval to resume launching from Launch Complex One.

With their investigation in its final stages and our launch license remaining active, we are fully anticipating to return to flight within the next few weeks.Following updates and changes to our testing and manufacturing processes, we will be returning to the pad with an even more reliable vehicle to meet our busy launch manifest for the remainder of ‘23 and into ‘24.

Now, let me take you through what happened and what we have learned.So here is a slide on the anomaly timeline.

The anomaly that ended the mission happened incredibly quickly.From the first action in the chain of events when Electron cutoff its data relay, the team only had 1.6 seconds of anomaly flight data to work with.

This was always going to be a highly complex issue to figure out, but with deep diligence and analysis, here is what we have been able to determine.On its 41st Mission launched September 19, from LC-1, it completed all the usual launch milestones through lift-off Max-Q stage separations.

At 151 seconds, the second stage engine tried to ignite, which is confirmed by flight telemetry that showed the ignited pressure is building and the locks and kerosene pump speed rising to pump propellants into the combustion chamber.The voltage levels from the battery packs that power the engine and the motor controllers were nominal at this point and normal at that point of ignition, but within milliseconds, in fact, 151.7 seconds, we get our first indication of the anomaly.

The system’s high level voltage levels take a sudden dip and rise of about 100 volts within 30 milliseconds, indicating an energy escape from a system that then led to a full loss of power to the second stage lower avionics, cutting off telemetry and communication with the second stage.And with that, it was all over.

So move on to the issues.So you have to bear with me on this was a little bit to talk about here.

But with good visual evidence with the on-boarded cameras and over 12,000 channels of data and this high level timeline to draw from, the investigation narrowed in on the issue.More than 200 sub-investigations were launched to rollout hypothetical causes of the anomaly.

After more than 7 weeks of extensive analysis of the mission’s manufacturing test and flight data, the findings of the Rocket Lab investigation team overwhelmingly indicate an unexpected electrical arc occurred within the power system.Shown in the image on the top right, the team did some tricky optical triangulation and image processing of a small shadow on the engine bell caused by the arc.

From that, they are able to pinpoint and retriangulate the failure’s points origin to an area where the two battery packs connect known as the fix-packed to supply the high voltage power.So now, we are all going to take a little lesson in passion law and passion curves.

So passion law describes how in partial pressure environments the likelihood of an act to occur changes in high voltage systems depending on the environmental composition.An approximate guide that can then be applied across different situations called the passion curve, which uses the relationship between voltage pressure, multiplied by distance to indicate what the range of danger is for an arc to form through various gases like helium, argon, nitrogen etcetera.

So the graph on the bottom right is what’s known as a highly simplified passion curves.So basically, the easiest way to think about this is if you have a positive in a negative terminal of a battery at 500 volts down here on earth, you could place those two terminals of the battery about 0.03 millimeters or one-third of the thickness of a human here beside each other and they would not create an arc or jumper spark between them.

Now, take the same 500-volt battery in terminals and put them in the worst part of the passion curve, which just happens to be just after stage separation and Stage 2 ignition of Electron and the same 500-volt battery in terminals will now act to each other when they are nearly 1 meter apart.So different gases, different pressures affect this distance.

And there is also other things like AC ripple that can have a huge negative effect.But for now, let’s just keep it simple.

For Electron, with its high voltage 500-volt power supply, we have to ensure that every connection is essentially hermetically sealed.A tiny pinprick or installation failure will result in arcs given that they can travel over large distances when in the passion curve.

One of this is influx and very transient, because as we ascend higher during the second stage burn and go into the high vacuum of space, the arcing distance goes back the other way and it becomes hard to arc again.It’s really just at stage separation where things are the worst and we bought them out on the passion curve.

As you can imagine, this is extremely difficult to test for down on earth.We actually currently put the whole rear engine assembly in a vacuum chamber, pull it down and inject gases like argon to try and aggravate the phenomenon.

But even the smallest installation compromise cannot always be detected, especially when you compile that with other factors like AC ripple and trace gases.Excuse me.

So, now that everybody understands passion curves during the second stage ignition, we are at the worst part of the curve and we had a small concentration of helium in the vicinity of the upper stage, which is normal and a high voltage AC ripple that lowers the spark threshold even lower and a tiny undetectable fault in the HV loom installation.All of which – excuse me, all of which combined allowed for an arc to briefly occur.

If any of these things were not present, then the failure would not have occurred.All four had to be there.

And to be honest, with all the testing we do before flight, you would also have to be incredibly unlucky to have the installation failure point, also line up with an electrical path to be able to act a chassis.And look, I don’t generally believe in luck as an engineer, but in this instance, I would say that so many things had to line up that most people would say that this – the current probability of this occurring would be largely improbable.

So with that, now that we kind of understand and we have explained the failure, what are we going to do to get back to flight?So the failure is obviously a highly complex set of conditions that are extremely difficult to predict.

A team’s top priority through the investigation has been to find a way to make sure that this never happens again.And as a result, there is a couple of key corrective measures.

The first is to increase the fidelity of a stage level vacuum testing.We now have a much more sensitive instruments implemented in the pre-flight test both at the component level and the stage level, that can sense partial discharge all the way down to a picocoulomb now.

This gives us much more confidence in the testing.However, I was not happy to stop there.

And so we have implemented a rather brute force solution.What we have done is seal up the battery frame, that contains all the high voltage connections and equipment and then pressurize, it to about 0.5 of PSI.

I will draw your attention to the graph on the top right.Surprise, surprise, it’s another passion curve that shows that by pressurizing the high voltage area, we shift the passion curve to the left out of the red zone and into the green zone, meaning basically, we are back to what it’s like on earth, where it’s not really possible for big archy distances to occur.

Now, this has been a lot of work to implement by the team and it’s a fairly extreme solution.But really, I thought of the only way we can put the passion law well back in its box.

So the best way to solve a problem in my opinion is always to eliminate the problem.And that’s what we have done.

Getting to the bottom of the issue and back to the pad for our customers has been the team’s number one priority.It’s been incredible to witness their perseverance, dedication over these past few weeks, not only on the anomaly investigation, but in the work that they have completed in parallel to make sure that we are good to go as soon as we get back to the pad.

The launch window for our return to flight mission will open on November 28 and extend into December.This dedicated mission will be for iQPS, a Japanese-based Earth imaging company, with the rocket for that mission going through pre-launch testing on the pad at launch complex right now.

So move on to Electron launch manifest.So in 2024, we have a really big year ahead of us.

Even with air pores in operations, Electron remains the world’s most frequently launch small orbital rocket.Dedicated missions for small satellites continue to experience strong demand, which we have seen in multiple buys by returning customers and constellation operators.

In fact, we have booked out Electron launches next year completely booked.We see the market for the Electron product being very strong and this manifest validates that.

Frequent launch opportunities, flexibility over schedule and control over orbiter deployment are what our customers are looking for and that’s what Electron has been providing and will continue to provide in the new year.And all that, all we have to do really in – with our 2024 manifest is execute as and with anything in the space industry.

By ramping Electron production and keeping on top of demand with recent acquisitions as well as continuous improvement in automation across our manufacturing processes, we look to continue improving on our already impressive performance in manufacturing.We also note that the scaling is coming with improved gross margins in Q3 2023, we achieved a 27% GAAP launch gross margin, which should look to enable to progress our profitability targets for Electron as we drive scale and efficiency into the business.

I now want to take you through and highlight some of their accomplishments in Q4.So Neutron Structures, we will start with a Neutron update.

Earlier this quarter, we reached a major milestone and had frosty second stage tank, up on the stand for structural and cryogenic testing, which is really a key marker for our Neutron program development, an embedded program.The team’s job was to push the tank to its absolute limits by loading it up with cryogenic fluids and test to destruction.

Something like 96,000 liters of liquid nitrogen was used for this test campaign and an exploded tank in this instance is very much a good thing and what we wanted to achieve.The team took the tank past me up or maximum expected operation pressure at more than 7x atmospheric pressure.

What they have learned in the campaign has been applied to the next Stage 2 tank and currently under production, really to vacant structural reliability early as we get closer to our date with the launch pad.Speaking of baking, this is quite literally what carbon composites team has been up to, with their next full scale Neutron structures and components.

The images on this slide here show you the scale of some of the in-tank devices being produced more than 7 feet in diameter for those circular propellant management devices and the Stage 2 dome being eliminated in the bottom section.Most of Neutron’s fixed fairing sections are coming together nicely.

And of course, we have another second stage Neutron Tank being built for our next test stint and – to go on our next test in the first half of ‘24.And then over to Neutron’s Archimedes engine, another test we are celebrating was a critical combustion test that the team achieved with Neutron’s Archimedes engine.

There is plenty of benefits to pursuing methane LOX propellants, but it does come with some of its own challenges.The critical piece really and one of the challenges was in using methane and liquid oxygen for Archimedes is getting the pre-burner dialed in, where generally you want a fuel mixture ratio in a chamber of something like 3:1 oxygen fuel, we are running an oxygen rich pre-burner cycle on Archimedes that forces us to flow all of our oxygen through the combustion device.

Therefore, our ideal mix is something between 60 to 100 to 1, which is a challenging thing to achieve without all the excess oxygen extinguishing combustion.Archimedes also has an extremely benign operating point, making it great for reliability and reusability, but it does mean that the pressures are low and ironically harder for the pre-burner.

But I am happy to say that we met all the operating points that we wanted to on those tests.That was a great accomplishment by the team.

At the same time, the Archimedes team had been producing and testing full scale hardware like valves, chambers, injectors, controllers and assemblies in preparation for development and propulsion tests making for a really impressive sight when all the pieces come together, like you see in the photo on the side as well.Over to Neutron infrastructure, so supporting infrastructure for Neutron has also scaled quickly over the past few months.

Ground works are being completed in Virginia, where our Neutron pad will be.Test facilities and support services will be based there as well.

And we are ready for construction to begin at our launch site located close to our key government customers, which will enjoy the benefits of a less congested launch site then obviously the case.In Q4, we opened our new engine development center in Long Beach that will support the development and production of the Archimedes engine.

And once the engines are completed at EDC, they will to go to testing at our standard NASA Stennis Space Center, where the Neutron team has been busy with site improvements to accept the engine for hot fires.And then finally, Neutron timeline, all of these achievements across Q3 and Q4 that I have mentioned and several others are shown here have been great to tick off along with – along the Neutron timeline.

We’ve completed second stage tank testing, printed key Archimedes engine parts and components had success with our combustion testing devices, completed qualification testing of our composite over our pressure vessel, run through separation lock deployment testing and stage pusher system testing, completed our actuator microcontroller testing, finished test on our power management module, confirm Neutron’s engine and stage controller functions that should completed avionics controller testing, successfully tested the vehicle’s thermal protection system, setup a test rig for incoming Neutron and system testing.The team is obviously working hard to keep our ambitious schedule for the rest of the year and into ‘24 with the same – with some of the next year milestones to look out for including first stage qualification tank test completed, Archimedes engine testing campaign and the first simulated flight orbit with our hardware connected to our flight computers.

Now, we will continue to provide updates on how Neutron is tracking outside our quarterly reviews.Beyond Electron and Neutron, our hypersonic test vehicle, HASTE has seen significant amounts of interest from new and returning government customers looking to further develop the nation’s hypersonic testing capability.

We have actually booked 7 launch contracts in the 6 months since HASTE program was introduced, including our latest mission announced today.HASTE launched from Virginia from the U.S Department of Defense Innovation Unit, this mission will demonstrate HASTE direct inject capability by deploying its payload during ascent, while still within the earth atmosphere, a long sought-after capability for the nation’s strategic defense and civil needs at a fraction of the cost of the current full scale tests.

On to space systems now and we have a new spacecraft order on the books for our confidential constellation customer that builds on a strong demand for our satellite products.This particular spacecraft will include a full suite of our own satellite components and subsystems, including star trackers reaction wheel solar panels, radios, flight software and so on and so forth.

This contract in particular speaks to the popularity and configurability of our spacecraft bus, but the confidence also in our satellite components in the market and our ability to grow an end-to-end mission grow as an end-to-end mission partner for the space industry.Now importantly, we will also be managing the mission’s operations and a further demonstration of our end-to-end business model of building and operating satellites that we build for our customers.

Continuous space systems to our largest space system contract now, the $143 million contract we have with MDA global staff.We are getting close to the delivery of our first of 17 spacecraft for the program by the end of Q1 next year.

Having cleared significant milestones in the contract in the past few months, the spacecraft critical design review and delivery of a structural thermal model for the customer, we expect to recognize revenue from those invoice payments to MDA in the fourth quarter of 2023.This sets the stage for a more meaningful revenue contribution from this contract as we enter 2024.

We continue to pursue increasingly complex and financially needle moving space system opportunities and are encouraged by progress being made in this part of our business.And we believe that these pursuits position us to continue scaling as an end-to-end space solutions leader.

Lastly, in space systems updates, we are proud to have directly supported the success of NASA’s groundbreaking Psyche mission launched in October, with their solar panels powering the spacecraft on its 6-year journey into deep space.These solar panels we provided to the mission hold the record for being the largest solar panels ever installed on a NASA JPL satellite, which we are immensely proud of.

And then finally into post-quarter achievements.I am thrilled to welcome retired U.S.

Space Force Lieutenant General, Nina Armagno to Rocket Lab’s Board of Directors.Lieutenant General Armagno served more than 35 years in leadership positions across the U.S.

Space Force and U.S.Space Force, including U.S Air Force and U.S.

Space Force including being the first Lieutenant General Officer appointed to and Director of Staff for the Space Force where she established America’s first new military branch in 72 years.She has had an accomplished and distinguished career in the military and will be an invaluable asset to the board.

And then over to Adam for the third quarter financial highlights.