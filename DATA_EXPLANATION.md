# Context
## Redshift
In physics, the redshift is a phenomenon where a generic electromagnetic radiation
(not necessarily red) from an object shows an increase in the wavelength. The opposite of a
redshift is a blueshift, where wavelengths shorten and energy increases. However, redshift is
a more common term and sometimes blueshift is referred to as negative redshift.  
The redshift is a quantity of interest in physics due to the phenomena that can cause it: 
1. objects move apart (or closer together) in space (doppler ffect); 
2. the space is expanding, causing objects to become separated (cosmological redshift); 
3. gravitational redshift is a relativistic effect observed due to strong gravitational fields.

## Photometric Letters

| Letter        | Wavelegth Midpoint (lambda) | Bandwidth (delta lambda) |
| -------       | --------------------------- | ------------------------ |
|U (ultraviolet)|365nm                        |66nm                      |
|B (blue)       |445nm                        |94nm                      |
|V (visible)    |551nm                        |88nm                      |
|R (red)        |658nm                        |138nm                     |
|I (infrared)   |806nm                        |149nm                     |

## Magnitudes
Magnitudes are inverted logarithmic measures of brightness. A galaxy with magnitude 21 (with
respect to a particular band) is 100-times brighter than one with magnitude 26.


# Dataset
Each row of the dataset represents a galaxy observation that is characterized by the following
attributes (one for each column, in this order):  

- **Nr**: ID number of the object observed;
- **Rmag, e.Rmag**: total red band magnitude (Rmag) and its error (e.Rmag). The error is
the standard deviation derived from detailed knowledge of the measurement process.
- **ApDRmag, mumax**: ApDRmag is the dfference between the total and aperture mag-
nitude in the R band. This is a rough measure of the size of the galaxy in the image
(ApDRmag=0 corresponds to a point source). Negative values are not physically meaning-
ful. mumax is the central surface brightness of the object in the R band. The difference
between Rmag and mumax should also be an indicator of galaxy size.
- **Mcz (target), e.Mcz, MCzml, chi2red**: Mcz and MCzml are two redshift estimates
(mean and peak of the distribution, respectively). Mcz is the preferred value; e.Mcz is its
estimated error and chi2red is the reduced chi-squared value of the least-squares fit of the
17-band magnitudes to the best-fit template galaxy spectrum.
- **UjMAG, e.UjMAG, ..., S280MAG, e.S280MAG** (col.10-29): these columns give
the absolute magnitudes of the galaxy in 10 bands with their measurement errors: Johnson
U, B, V; Bessel U, B, V; SDSS u, g (i.e. green), r; other (S280). They are based on the
measured magnitudes and represent the luminosities of the galaxies. These magnitudes are
not all independent of each others, but the are important for representing intrinsic properties
of the galaxies.
- **W420FE, e.W420FE, ..., W914FE, e.W914FE** (col.30-55): these columns observe
the brightnesses in 13 bands in sequence from 420 nm in the ultraviolet to 915 nm in
the far red. These are given in linear variables with units of photon 
ux densities. Each
measurement is accompanied by an error.
- **UFS, e.UFS, ..., IFD, e.IFD**: observed brightnesses in the five traditional broad spectral
bands, UBVRI. These data can be largely redundant with the 13 bands in the previous
columns.

# Author
This brief explanation of the dataset is provided in the course material from Politecnico di Torino.