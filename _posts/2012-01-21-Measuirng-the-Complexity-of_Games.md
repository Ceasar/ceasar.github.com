---
layout: post
title: Measuring the Complexity of Games
---

Let me preface right away by saying I am by no means an expert on the subject. (Which is to say, though the field is narrow, there are some experts on the subject who know way more than me.)


Introduction
============

My younger brother, Max, is in 8th grade. Like others his age, he likes playing video games, and for Christmas last year, he recieved many and I (somewhat unwillingly) got the chance to watch.

One game that he played quite a bit of was Call of Duty: Modern Warfare 2. As you might expect, it's your typical run and gun shooter with no outstanding qualities except that its extremely popular among teenagers.

What intrigued me most about it though, was how fast Max picked it up. Obviously, with nothing better to do he spent more time on it in a single day than most might have in a week, but nevertheless, withing a week, he had taken the game as far as he could and regularly was on the top of the leaderboard.

We also got a chance to revive Halo: Reach, also a shooter, but in my opinion far more complex. I spent a few hours playing myself, and noticed my skill level increasing very slowly, if at all.

Which got me thinking-- mastering MW2 is really no feat at all. The difference between the worst and the best players in MW2 is much smaller than it is in Halo. In effect, there is a way to measure the complexity of games. And more importantly, if we could figure out how to increase complexity, we can presumably create more interesting games.


Measuring Complexity
====================

To measure complexity, it's important to first understand the unit by which we measure. Unfortunately, there is no standard way of doing so. Like measuring the complexity of algorithms, where both memory and speed, two orthogonal features, are considered, measuring the complexity of games also requires measuring multiple components.

The simplest, and most intuitive measure, is the state-space complexity, or the number of legal game positions reachable from the initial positions of the game. Though hard to calculate in practice, it often provides a useful upper bound by which to compare.

A second measure is the size of the game tree, or the total number of possible games that can be played. This measure is slightly more interesting, because often a state of the game can be reached via multiple routes. It also, however, suffers the drawback of being less interesting when a position is repeatable. It's worthing noting that the size of the game tree is orders of magnitude greater than the state-space.


Some Examples
=============

Let's start with a simple example: Tic-Tac-Toe.

The upper bound for the state-space complexity of tic-tac-toe is simply 3^9 or 19,683, since there are three states for each cell, and nine cells. he includes many illegal positions and positions not reachable by the rules. Removing illegal positions give only 5,478, and when reflections and rotations are removed, there are only 765 unique possible games.

Now let's take Checkers. There are 16 squares and 5 possible states, so that gives us an upperbound on the state-space complexity of 5^16, or 152,587,890,625-- vastly larger than Tic-Tac-Toe.

For Chess, there are 64 squares and 7 possible states per square, so 7^64 is the upperbound of the state-space complexity.

And for Go, played on a 13x13 board, there are 169 squares and 3 possible states, which gives us an astronmical 3^169 possible states.

Of course, for many modern games, these measures don't exactly apply as they are played in real-time rather than in turns, moving them up to a completely higher level.


A Better Measure?
=================

Now obviously, you may be wondering how it is that Max could beat 99% of players withing a weak when playing a, according to our measures, game infinitely more complex than chess. Clearly, something is off.

As it turns out, there is a more interesting way to measure complexity, and it's closely related to A* (or minimax for those more familiar). Instead of measuring the number of possible states or possible games, an alternative way is to measure how long it takes to find the optimal way to play a game. This is known as the decision complexity of a game.

As gamers know, amateur designers often try to increase the complexity of their games by increasing the number of options available to a player. Many games for example, offer endless options to customize a character- imagine thousands of options for choice of sword, helmet, breast-plate, shield, etc.

As it turns out though, this almost never works. Gamers are highly resourceful, not unlike ants, and they quickly find near optimal solutions, rendering most options utterly useless.

Thus, though at anytime Max might have to choose between an infinite number of ways to move his character, in reality, his choices are often quite few.

(More experienced designers fix this problem by limiting the number of options available, but working hard to ensure they are meaningful and equally valuable ("balanced"). Some object that this approach reduces the fun of discovering what works well and what doesn't, but others argue that customization is rarely the core component of a game.)


How Then, Can We Increase Complexity?
============================

If increasing the state-space does not increase complexity, what does?

It's hard to say. I don't really have an answer. But there are some common mistakes I notice that are easily avoided.

* Focus on adding more dimensions, not more vectors. Many games, MW2 included, think they are making the game more interesting by adding more guns and simply changing up the stats. The fact is they are not-- Only the over-arching classes of weapons actually ever mattered, and the differences between them may as well been scrapped. (In other words, offering five sniper rifles is pointless. The differences are so minimal it makes no signficant difference.) Halo, among others, avoids this antipattern quite effectively, with each gun being quite different from the next (although admittedly, some still get very little use). I should add that the easiest way to do this is to simply not reveal any numbers to the player unless absoultely neccesary. Offering numbers seems to encourage this vector-based behavior.
* Actively search out game-breaking features, and eliminate them. The perhaps most classic example, is the en-passant rule in Chess. Without this rule, many end-games would be trivial, as a player could start a race for promotion without any resistance. Notice that though the rule at first glance appears to constrain the number of games possible, it actually does the reverse by making more options viable.
* As a corrolary to the above, the obvious implication is to encourage patience, or equivalently, long-term strategies. When Deep Blue challenged Gary Kasparov, Kasparov was able to beat the machine by taking advantage of its sole weakness: Though it could analyze hundreds of moves ahead, it was impossible to devise the machine to be able to evaluate a position correctly. Thus, Kasparov played extremely patiently, playing boring defensive games and commiting to extremely positional play. Kasparov, of course, won. (Take a step back and think about that for a second.)
* Day[9] refers to this ability as understanding the marginal advantage. He articles describes how the ability to recognize these slight advantages is what distinguishes the pros from everybody else. Interestingly, why these marginal advantages are how the pros distinguish themselves, the large gap between the best and the worst is largely on account of tactical victories.
* Maximize tradeoffs. Attempting to play chess positionally is recommended against by most chess experts when teaching chess newbies. Instead they emphasize recognizing patterns that lead to decisive victories (as opposed to marginal ones). The reason why is simple: to win positionally requires a deep understanding of the game- often times, players have to choose between a variety of moves, each of which offer utility, but in different dimensions. That is, one move may grant an immediate advantage, and another may grant an advantage if five turns from now. How does one choose? The only reasonable answer in these cases is to try both. In games like Halo, players are regularly confronted with these choices- do I grab the enemy flag now, or do I first try to kill everyone in the room? Do I trade my Battle Rifle for this grenade launcher? These decisions rarely have an obvious right answer, and that makes it that much harder to figure out which one is truly best.
