/*
 *  Delphes: a framework for fast simulation of a generic collider experiment
 *  Copyright (C) 2012-2014  Universite catholique de Louvain (UCL), Belgium
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef ConstituentFilter_h
#define ConstituentFilter_h

/** \class ConstituentFilter
 *
 *  Drops all input objects that are not constituents of any jet.
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"

#include <map>
#include <vector>

class TIterator;
class TObjArray;

class ConstituentFilter: public DelphesModule
{
public:
  ConstituentFilter();
  ~ConstituentFilter();

  void Init();
  void Process();
  void Finish();

private:
  Double_t fJetPTMin;

  std::vector<TIterator *> fInputList; //!

  std::map<TIterator *, TObjArray *> fInputMap; //!

  TObjArray *fOutputArray; //!

  ClassDef(ConstituentFilter, 1)
};

#endif
