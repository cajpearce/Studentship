# efg, Stowers Institute for Medical Research, July 2004
# Updated 26 May 2005
#
# Lomb-Scargle Normalized Periodogram
#
# from
# "Fast Algorithm for Spectral Analysis of Unevenly Sampled Data"
# Astrophysical Journal, 338:277-280, March 1989.
# William H. Press and George B. Rybicki.
#
# Also appeared in Section 13.8, "Spectral Analysis of Unevenly
# Sampled Data" in Numerical Recipes in C (2nd Ed), William H. Pres,
# et al, Cambridge University Press, 1992.

LombScargle <- function(t, h, TestFrequencies, Nindependent)
{
  stopifnot( length(t) == length(h) )

  hResidual    <- h - mean(h)

  SpectralPowerDensity <- rep(0, length(TestFrequencies))

  for (i in 1:length(TestFrequencies))
  {
    Omega       <- 2*pi*TestFrequencies[i]
    TwoOmegaT   <- 2*Omega*t
    Tau         <- atan2( sum(sin(TwoOmegaT)) , sum(cos(TwoOmegaT))) /
                   (2*Omega)
    OmegaTMinusTau <- Omega * (t - Tau)
    SpectralPowerDensity[i] <- (sum (hResidual * cos(OmegaTMinusTau))^2) /
                                sum( cos(OmegaTMinusTau)^2 ) +
                               (sum (hResidual * sin(OmegaTMinusTau))^2) /
                                sum( sin(OmegaTMinusTau)^2 )
  }

  # The "normalized" spectral density refers to the variance term in the
  # denominator.  With this term the SpectralPowerDensity has an
  # exponential probability distribution with unit mean.
  SpectralPowerDensity <- SpectralPowerDensity / ( 2 * var(h) )

  Probability <- 1 - (1-exp(-SpectralPowerDensity))^Nindependent

  PeakIndex    <- match(max(SpectralPowerDensity), SpectralPowerDensity)
  LikelyPeriod <- 1 / TestFrequencies[PeakIndex]
  LikelyPvalue <- Probability[PeakIndex]

  return( list( Probability=Probability,
                SpectralPowerDensity=SpectralPowerDensity,
                PeakIndex=PeakIndex,
                LikelyPeriod=LikelyPeriod,
                LikelyPvalue=LikelyPvalue
              ) )
}

########################################################################

# Compute Lomb-Scargle Periodogram
N <- 20
tDelta <- 6           # minutes
t <- 0:(N-1) * tDelta # minutes
period <- 120         # minutes
frequency <- 1/period
ExpressionProfile <- cos(2*pi*frequency*t)

M <- 4*N              # Often use 2N or 4N test frequencies

# Only use test frequencies that correspond to periods from
# 30 to 180 minutes.
TestFrequencies <- TestFrequencies <- (1/180) + (1/30 - 1/180)* 0:(M-1) / (M-1)

Nindependent <- N     # Approximation

LS <- LombScargle(t, ExpressionProfile, TestFrequencies, Nindependent)
print(LS)

########################################################################

# Show results graphically as suggested by MatLab code found on the
# Woods Hole Oceanographic Institution web site:
# http://w3eos.whoi.edu/12.747/notes/lect07/l07s05.html

savepar <- par(mfrow=c(2,2))  # 2 rows by 2 columns of graphics

# 1. Original data curve
plot(t, ExpressionProfile,
     "o", col="Blue", ylab="Cosine Curve", xlab="Time [minutes]",
     main=paste(c("Cosine (N =",N,")"), collapse=" "))

# 2. Measure of uneveness of intervals
hist(log10(diff(t)), xlim=c(-6,6),
     xlab="log10(delta T)",
     main="Time Interval Variability")

# 3. Lomb-Scargle Periodogram
plot(TestFrequencies, LS$SpectralPowerDensity,
     "o", col="Red",
     ylab="Normalized Power Spectral Density", xlab="Frequency [1/minute]",
     main="Lomb-Scargle Periodogram",
     ylim=c(0,10))
text(TestFrequencies[LS$PeakIndex], LS$SpectralPowerDensity[LS$PeakIndex],
     paste("period = ", round(LS$LikelyPeriod,1), " minutes"),
     pos=TEXT_RIGHT<-4)
points(TestFrequencies[LS$PeakIndex], LS$SpectralPowerDensity[LS$PeakIndex],
     pch=19, col="Red")


# 4. Probability (significance of peak)
plot(TestFrequencies, LS$Probability,
     "o", col="Red",
     ylab="Probability", xlab="Frequency [1/minute]",
     main="Peak Significance",
     ylim=c(0,1))
text(TestFrequencies[LS$PeakIndex], LS$Probability[LS$PeakIndex],
     paste("p = ", round(LS$LikelyPvalue,4)),
     pos=TEXT_ABOVE<-3)
points(TestFrequencies[LS$PeakIndex], LS$Probability[LS$PeakIndex],
     pch=19, col="Red")

par(savepar)
