#ifndef  UTILS_ANALYZERS_H
#define  UTILS_ANALYZERS_H


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
      template<typename V> inline void Mag2(V (&vec)) {
        vec[0] = vec[1]*vec[1] + vec[2]*vec[2] + vec[3]*vec[3];
      }
    }

    /// @}
  }
}

#endif
