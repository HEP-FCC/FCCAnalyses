// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/Utils.h"

namespace LHAPDF {

  namespace {

    /// @todo Tidy up
    static const double kMACHEP = 1.11022302462515654042363166809e-16;
    static const double kMAXLOG = 709.782712893383973096206318587;
    static const double kBig = 4.503599627370496e15;
    static const double kBiginv =  2.22044604925031308085e-16;

    double igamc(double a, double x);
    double igam(double a, double x);

    /// @name gamma functions from Cephes library -- http://www.netlib.org/cephes
    ///
    /// Copyright 1985, 1987, 2000 by Stephen L. Moshier
    //@{

    /// @brief Incomplete gamma function (complement integral)
    ///
    /// \f$ \gamma_c(a,x) = 1 - \gamma(a,x) \f$
    /// \f$ \gamma_c(a,x) = 1/\Gamma(a) \int_x^\inf e^-t t^(a-1) dt \f$
    ///
    /// In this implementation both arguments must be positive.
    /// The integral is evaluated by either a power series or
    /// continued fraction expansion, depending on the relative
    /// values of a and x.
    double igamc(double a, double x) {
      double ans, ax, c, yc, r, t, y, z;
      double pk, pkm1, pkm2, qk, qkm1, qkm2;

      // LM: for negative values returns 0.0
      // This is correct if a is a negative integer since Gamma(-n) = +/- inf
      if (a <= 0)  return 0.0;

      if (x <= 0) return 1.0;

      if( (x < 1.0) || (x < a) )
        return( 1.0 - igam(a,x) );

      ax = a * log(x) - x - lgamma(a);
      if( ax < -kMAXLOG )
        return( 0.0 );

      ax = exp(ax);

      // Continued fraction
      y = 1.0 - a;
      z = x + y + 1.0;
      c = 0.0;
      pkm2 = 1.0;
      qkm2 = x;
      pkm1 = x + 1.0;
      qkm1 = z * x;
      ans = pkm1/qkm1;

      do
        {
          c += 1.0;
          y += 1.0;
          z += 2.0;
          yc = y * c;
          pk = pkm1 * z  -  pkm2 * yc;
          qk = qkm1 * z  -  qkm2 * yc;
          if(qk)
            {
              r = pk/qk;
              t = fabs( (ans - r)/r );
              ans = r;
            }
          else
            t = 1.0;
          pkm2 = pkm1;
          pkm1 = pk;
          qkm2 = qkm1;
          qkm1 = qk;
          if( fabs(pk) > kBig )
            {
              pkm2 *= kBiginv;
              pkm1 *= kBiginv;
              qkm2 *= kBiginv;
              qkm1 *= kBiginv;
            }
        }
      while (t > kMACHEP);

      return ans*ax;
    }


    /// @brief Left tail of incomplete gamma function
    ///
    /// \f$ \gamma(a,x) = x^a e^-x \sum_k=0^\inf x^k / \Gamma(a+k+1) \f$
    double igam( double a, double x )
    {
      double ans, ax, c, r;

      // LM: for negative values returns 1.0 instead of zero
      // This is correct if a is a negative integer since Gamma(-n) = +/- inf
      if (a <= 0)  return 1.0;

      if (x <= 0)  return 0.0;

      if( (x > 1.0) && (x > a ) )
        return( 1.0 - igamc(a,x) );

      /* Compute  x**a * exp(-x) / gamma(a)  */
      ax = a * log(x) - x - lgamma(a);
      if( ax < -kMAXLOG )
        return( 0.0 );

      ax = exp(ax);

      /* power series */
      r = a;
      c = 1.0;
      ans = 1.0;

      do
        {
          r += 1.0;
          c *= x/r;
          ans += c;
        }
      while( c/ans > kMACHEP );

      return( ans * ax/a );
    }

    //@}

  }



  /// @brief Compute quantiles for standard normal distribution N(0, 1) at probability p
  ///
  /// ALGORITHM AS241  APPL. STATIST. (1988) VOL. 37, NO. 3, 477-484.
  double norm_quantile(double p) {

    /// @todo Return +-inf
    if (p <=0 || p >= 1) {
      cerr << "norm_quantile: probability outside (0, 1)" << endl;
      return 0;
    }

    const double  a0 = 3.3871328727963666080e0;
    const double  a1 = 1.3314166789178437745e+2;
    const double  a2 = 1.9715909503065514427e+3;
    const double  a3 = 1.3731693765509461125e+4;
    const double  a4 = 4.5921953931549871457e+4;
    const double  a5 = 6.7265770927008700853e+4;
    const double  a6 = 3.3430575583588128105e+4;
    const double  a7 = 2.5090809287301226727e+3;
    const double  b1 = 4.2313330701600911252e+1;
    const double  b2 = 6.8718700749205790830e+2;
    const double  b3 = 5.3941960214247511077e+3;
    const double  b4 = 2.1213794301586595867e+4;
    const double  b5 = 3.9307895800092710610e+4;
    const double  b6 = 2.8729085735721942674e+4;
    const double  b7 = 5.2264952788528545610e+3;
    const double  c0 = 1.42343711074968357734e0;
    const double  c1 = 4.63033784615654529590e0;
    const double  c2 = 5.76949722146069140550e0;
    const double  c3 = 3.64784832476320460504e0;
    const double  c4 = 1.27045825245236838258e0;
    const double  c5 = 2.41780725177450611770e-1;
    const double  c6 = 2.27238449892691845833e-2;
    const double  c7 = 7.74545014278341407640e-4;
    const double  d1 = 2.05319162663775882187e0;
    const double  d2 = 1.67638483018380384940e0;
    const double  d3 = 6.89767334985100004550e-1;
    const double  d4 = 1.48103976427480074590e-1;
    const double  d5 = 1.51986665636164571966e-2;
    const double  d6 = 5.47593808499534494600e-4;
    const double  d7 = 1.05075007164441684324e-9;
    const double  e0 = 6.65790464350110377720e0;
    const double  e1 = 5.46378491116411436990e0;
    const double  e2 = 1.78482653991729133580e0;
    const double  e3 = 2.96560571828504891230e-1;
    const double  e4 = 2.65321895265761230930e-2;
    const double  e5 = 1.24266094738807843860e-3;
    const double  e6 = 2.71155556874348757815e-5;
    const double  e7 = 2.01033439929228813265e-7;
    const double  f1 = 5.99832206555887937690e-1;
    const double  f2 = 1.36929880922735805310e-1;
    const double  f3 = 1.48753612908506148525e-2;
    const double  f4 = 7.86869131145613259100e-4;
    const double  f5 = 1.84631831751005468180e-5;
    const double  f6 = 1.42151175831644588870e-7;
    const double  f7 = 2.04426310338993978564e-15;

    const double split1 = 0.425;
    const double split2=5.;
    const double konst1=0.180625;
    const double konst2=1.6;

    double q, r, quantile;
    q = p - 0.5;
    if (fabs(q) < split1) {
      r = konst1 - q*q;
      quantile = q* (((((((a7 * r + a6) * r + a5) * r + a4) * r + a3)
                       * r + a2) * r + a1) * r + a0) /
        (((((((b7 * r + b6) * r + b5) * r + b4) * r + b3)
           * r + b2) * r + b1) * r + 1.);
    } else {
      r = (q < 0) ? p : 1-p;
      //error case
      if (r<=0)
        quantile=0;
      else {
        r=sqrt(-log(r));
        if (r<=split2) {
          r=r-konst2;
          quantile=(((((((c7 * r + c6) * r + c5) * r + c4) * r + c3)
                      * r + c2) * r + c1) * r + c0) /
            (((((((d7 * r + d6) * r + d5) * r + d4) * r + d3)
               * r + d2) * r + d1) * r + 1);
        } else{
          r=r-split2;
          quantile=(((((((e7 * r + e6) * r + e5) * r + e4) * r + e3)
                      * r + e2) * r + e1) * r + e0) /
            (((((((f7 * r + f6) * r + f5) * r + f4) * r + f3)
               * r + f2) * r + f1) * r + 1);
        }
        if (q<0) quantile=-quantile;
      }
    }
    return quantile;
  }


  /// @brief Compute quantiles of the chi-squared probability distribution function
  ///
  /// Algorithm AS 91   Appl. Statist. (1975) Vol.24, P.35
  /// implemented by Anna Kreshuk.
  /// Incorporates the suggested changes in AS R85 (vol.40(1), pp.233-5, 1991)
  /// Parameters:
  ///   @arg p   - the probability value, at which the quantile is computed
  ///   @arg ndf - number of degrees of freedom
  double chisquared_quantile(double p, double ndf) {
    static const double c[] = {0, 0.01, 0.222222, 0.32, 0.4, 1.24, 2.2,
                               4.67, 6.66, 6.73, 13.32, 60.0, 70.0,
                               84.0, 105.0, 120.0, 127.0, 140.0, 175.0,
                               210.0, 252.0, 264.0, 294.0, 346.0, 420.0,
                               462.0, 606.0, 672.0, 707.0, 735.0, 889.0,
                               932.0, 966.0, 1141.0, 1182.0, 1278.0, 1740.0,
                               2520.0, 5040.0};
    static const double e = 5e-7;
    static const double aa = 0.6931471806;
    static const int maxit = 20;

    /// @todo Tidy
    double ch, p1, p2, q, t, a, b, x;
    double s1, s2, s3, s4, s5, s6;

    if (ndf <= 0) return 0;

    const double g = lgamma(0.5*ndf);
    const double xx = 0.5 * ndf;
    const double cp = xx - 1;

    if (ndf >= log(p)*(-c[5])){
      // Starting approximation for ndf less than or equal to 0.32
      if (ndf > c[3]) {
        x = norm_quantile(p);
        // Starting approximation using Wilson and Hilferty estimate
        p1 = c[2]/ndf;
        ch = ndf*pow((x*sqrt(p1) + 1 - p1), 3);
        if (ch > c[6]*ndf + 6)
          ch = -2 * (log(1-p) - cp * log(0.5 * ch) + g);
      } else {
        ch = c[4];
        a = log(1-p);
        do {
          q = ch;
          p1 = 1 + ch * (c[7]+ch);
          p2 = ch * (c[9] + ch * (c[8] + ch));
          t = -0.5 + (c[7] + 2 * ch) / p1 - (c[9] + ch * (c[10] + 3 * ch)) / p2;
          ch = ch - (1 - exp(a + g + 0.5 * ch + cp * aa) *p2 / p1) / t;
        } while (fabs(q/ch - 1) > c[1]);
      }
    } else {
      ch = pow((p * xx * exp(g + xx * aa)),(1./xx));
      if (ch < e) return ch;
    }
    // Call to algorithm AS 239 and calculation of seven term Taylor series
    for (int i = 0; i < maxit; ++i) {
      q = ch;
      p1 = 0.5 * ch;
      p2 = p - igam(xx, p1);

      t = p2 * exp(xx * aa + g + p1 - cp * log(ch));
      b = t / ch;
      a = 0.5 * t - b * cp;
      s1 = (c[19] + a * (c[17] + a * (c[14] + a * (c[13] + a * (c[12] +c[11] * a))))) / c[24];
      s2 = (c[24] + a * (c[29] + a * (c[32] + a * (c[33] + c[35] * a)))) / c[37];
      s3 = (c[19] + a * (c[25] + a * (c[28] + c[31] * a))) / c[37];
      s4 = (c[20] + a * (c[27] + c[34] * a) + cp * (c[22] + a * (c[30] + c[36] * a))) / c[38];
      s5 = (c[13] + c[21] * a + cp * (c[18] + c[26] * a)) / c[37];
      s6 = (c[15] + cp * (c[23] + c[16] * cp)) / c[38];
      ch = ch + t * (1 + 0.5 * t * s1 - b * cp * (s1 - b * (s2 - b * (s3 - b * (s4 - b * (s5 - b * s6))))));
      if (fabs(q / ch - 1) > e) break;
    }
    return ch;
  }


}
