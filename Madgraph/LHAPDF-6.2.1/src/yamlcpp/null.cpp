#include "yaml-cpp/null.h"
#include "yaml-cpp/node.h"

namespace LHAPDF_YAML
{
	_Null Null;

	bool IsNull(const Node& node)
	{
		return node.Read(Null);
	}
}
