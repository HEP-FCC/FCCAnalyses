// -*- C++ -*-
//
// This file is part of LHAPDF
// Copyright (C) 2012-2016 The LHAPDF collaboration (see AUTHORS for details)
//
#include "LHAPDF/Interpolator.h"
#include "LHAPDF/GridPDF.h"

namespace LHAPDF {


double Interpolator::interpolateXQ2(int id, double x, double q2) const {
      // Subgrid lookup
      /// @todo Do this in two stages to cache the KnotArrayNF?
      /// @todo Add flavour error checking

      const KnotArray1F& subgrid = pdf().subgrid(id, q2);
      // Index look-up
      /// @todo Cache this index lookup for performance?
      // cout << "From Ipol: x = " << x << ", Q2 = " << q2 << endl;
      const size_t ix = subgrid.ixbelow(x);
      const size_t iq2 = subgrid.iq2below(q2);
      // cout << "ix = " << ix << ", iq2 = " << iq2 << ", xf[ix, iq2] = " << subgrid.xf(ix, iq2) << endl;
      /// Call the overloaded interpolation routine on this subgrid
      return _interpolateXQ2(subgrid, x, ix, q2, iq2);
    }


}
