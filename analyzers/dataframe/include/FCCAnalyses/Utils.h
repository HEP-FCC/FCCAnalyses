#ifndef  UTILS_ANALYZERS_H
#define  UTILS_ANALYZERS_H

#include <cmath>

namespace FCCAnalyses {
  namespace Utils {

    template<typename T> inline auto getsize( T& vec){ return vec.size();};

    /**
     *   \addtogroup Vec3
     *   @{
     */

    /**  Set of utilities to work with 3-vectors. Four elements are expected:
     *   0: magnitude squared
     *   1: x value
     *   2: y value
     *   3: z value
     */
    namespace Vec3 {
      template<typename V>
      inline void Mag2(V (&vec)[4]) {
        vec[0] = vec[1]*vec[1] + vec[2]*vec[2] + vec[3]*vec[3];
      }

      template<typename V>
      inline V Dot(V vec1[4], V vec2[4]) {
        return vec1[1]*vec2[1] + vec1[2]*vec2[2] + vec1[3]*vec2[3];
      }

      template<typename V>
      inline void Cross(V (&vec)[4], V vec1[4], V vec2[4]) {
        vec[1] = vec1[2]*vec2[3] - vec1[3]*vec2[2];
        vec[2] = vec1[3]*vec2[1] - vec1[1]*vec2[3];
        vec[3] = vec1[1]*vec2[2] - vec1[2]*vec2[1];
      }

      template<typename V>
      inline void Unit(V (&vec)[4]) {
        V mag = std::sqrt(vec[0]);
        vec[1] = vec[1]/mag;
        vec[2] = vec[2]/mag;
        vec[3] = vec[3]/mag;
      }

      template<typename V>
      inline void Plus(V (&vec)[4], V vecIn1[4], V vecIn2[4]) {
        vec[1] = vecIn1[1] + vecIn2[1];
        vec[2] = vecIn1[2] + vecIn2[2];
        vec[3] = vecIn1[3] + vecIn2[3];
      }

      template<typename V>
      inline void Minus(V (&vecOut)[4], V vecIn1[4], V vecIn2[4]) {
        vecOut[1] = vecIn1[1] - vecIn2[1];
        vecOut[2] = vecIn1[2] - vecIn2[2];
        vecOut[3] = vecIn1[3] - vecIn2[3];
      }

      template<typename V>
      inline void Copy(V (&vecOut)[4], V vecIn[4]) {
        vecOut[0] = vecIn[0];
        vecOut[1] = vecIn[1];
        vecOut[2] = vecIn[2];
        vecOut[3] = vecIn[3];
      }
    }

    /// @}
  }
}

#endif
