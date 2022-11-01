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

#ifndef DelphesDisplay_h
#define DelphesDisplay_h

class TEveProjectionManager;
class TEveElement;
class TEveCalo3D;
class TEveCaloLego;
class TEveViewer;
class TEveScene;

class DelphesDisplay
{
public:
  DelphesDisplay();

  virtual ~DelphesDisplay();

  void ImportGeomRPhi(TEveElement *el);
  void ImportGeomRhoZ(TEveElement *el);

  void ImportCaloRPhi(TEveCalo3D *calo);
  void ImportCaloRhoZ(TEveCalo3D *calo);
  void ImportCaloLego(TEveCaloLego *calo);

  void ImportEventRPhi(TEveElement *el);
  void ImportEventRhoZ(TEveElement *el);

  void DestroyEventRPhi();
  void DestroyEventRhoZ();

private:
  TEveProjectionManager *fRPhiMgr;
  TEveProjectionManager *fRhoZMgr;

  TEveViewer *fRPhiView;
  TEveViewer *fRhoZView;
  TEveViewer *f3DimView;
  TEveViewer *fLegoView;

  TEveScene *fRPhiGeomScene;
  TEveScene *fRhoZGeomScene;

  TEveScene *fRPhiCaloScene;
  TEveScene *fRhoZCaloScene;
  TEveScene *fLegoCaloScene;

  TEveScene *fRPhiEventScene;
  TEveScene *fRhoZEventScene;
};

#endif /* DelphesDisplay_h */
