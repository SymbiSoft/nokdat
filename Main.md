# Introduction #
This program is aimed to make any python-supporting cellphone equipped with a camera to be used as a data logger for devices equipped with LCD displays.


# Details #

There are a lot of devices around capable of measuring and showing several informations: temperature, humidity, power consumption, objects counted, and so on. Most of them, not designed for professional use, are not capable of storing any of the data they show: once data are measured and shown, then they're "gone".

Professional devices capable of storing same data costs ten times much.

But a solution could come from old nokia series60 phone, which can be bought in the second-hand market for around 50 bucks: these phones have built-in camera, and they support python programming; so it's just a matter of writing the proper software to recognize character displayed on LCD of devices; this process is usually known as Optical Character Recognition, but it looks like no OCR program available on the market is designed to recognize LCD characters, nor for PC neither for cellphones.

# How to #

The "mental process", i.e. the "algorithm", we use to recognize LCD numbers is very easy: if an area of the display is dark, we "get it" as an "on segment"; if it is white, the segment is off; by combining 7 segment it is possibile to obtain all the ten digits we need (and some more alphabetic characters).

So, how to "teach" this to a PC or a cellphone?

The biggest difficulty is taking into account different brightness of the same image in different areas: this lead to having an "off segment" as dark as an "on segment" in a brighter area of the same image, thus completely confusing the software, which is not able to properly detect which segments are on and which off.

So, just comparing area brightness to a predefined brightness threshold is not enough.
I'm currently investigating how to compare the brightness of a segmento to the adiacent area: this should allow recognizing an off or on segment regardless of area brightness.

Work is still in progress, and any help is appreciated...