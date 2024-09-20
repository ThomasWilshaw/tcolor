# TColour (TC)

## Overview
A small proof of concept library that allows users to build colour spaces from small reuseable chunks as opposed to creating monolithic config files

## Basic Assumptions

- That three channel wattages as encodings, decodings, and interstitial states, should be described and characterized in an unambiguous fashion.
- All colour spaces require at minimum three components:
    1. Three primaris
    2. A white point
    3. A transfer function

 ## What TColour Is Trying To  Avoid
- Recursion. Including a colourimetric library or references / schema of another colourimetric library or protocol that burdens the NC library with potentially unwanted dependencies.
- Abstractions. Overly complex conceptual models that prohibit or inhibit clear and direct communication of colourimetric wattage states.
- Brittleness. Hard-coded or strict implementation models that prohibit or inhibit proper decoding and interpretation of the encoded or assumed colourimetric states.

## Encoding and Decoding Characterization States

Encodings may arrive or be assumed to be in a plethora of states. This might include varying file encodings, variable technical encoding characteristics, and varying colourimetric metadata and information.

To this end, as an introductory schema attempting to gain a solid foundation, a core assumption of an RGB encoding model is assumed for the following rationale:

- It is the common language of imagery.
- It is the most common pre-encoding and post-decoding state.
- It is the basis of a majority of display encodings and decodings.
- An RGB encoding has a direct relationship to the ground truth for all colourimetric information via the CIE’s XYZ fundamental relative wattage metric.
  
It is understood that assumptions of an RGB encoding model, while covering a large number of usage contexts, is ultimately limited. As an introductory approach however, it is a reasonable starting point.

## The RGB Encoding Model
According to the CIE, [an additive RGB encoding model](https://www.iso.org/standard/37161.html) requires three pieces of metadata to fully describe a colourimetric signal:

- A set of three unique primaries, described using a Standard Observer colourimetric model.
- A description of a centroid, described using a Standard Observer colourimetric model.
- Transfer characteristics that describe the encoding’s relationship with respect to a tristimulus relative wattage ground truth.

Without these three concrete pieces of information, an RGB encoding is ambiguous, and any and all transforms applied upon the RGB values will be equally ambiguous.

## Metadata Schema Overview
- Descriptor.
- Red, Green, and Blue primaries expressed in CIE xy chromaticity coordinates.
- Achromatic centroid primary expressed in CIE xy chromaticity coordinates.
- Transfer function expressed in either a sidecar LUT file descriptor, or a selection of communal and strictly defined colourimetric component transfer characteristics (power law, power law with linear section etc.).
- A high level default CIE colourimetry version, consisting of either the assumed default of 1931 CIE XYZ model, or the more contemporary 2015 CIE XYZ model definition.
- Alaises that can also be used to identify the colour space
- An dictionary of other useful information

Full docs will be provided at a later state if and when things are more stable
