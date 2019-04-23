from __future__ import unicode_literals

import pytest
from lark.exceptions import LarkError

from dj_rql.constants import RQL_ORDERING_OPERATOR
from dj_rql.parser import RQLParser
from tests.test_parser.constants import FAIL_PROPS, OK_PROPS
from tests.test_parser.utils import OrderingTransformer


REVERSED_OK_PROPS = reversed(OK_PROPS)


def ordering_transform(props):
    query = '{operator}({props})'.format(
        operator=RQL_ORDERING_OPERATOR, props=','.join(props),
    )
    return OrderingTransformer().transform(RQLParser.parse(query))


@pytest.mark.parametrize('p1,p2', zip(OK_PROPS, REVERSED_OK_PROPS))
def test_ordering_ok(p1, p2):
    assert ordering_transform(('+{}'.format(p1),)) == (p1,)
    assert ordering_transform(('-{}'.format(p2),)) == ('-{}'.format(p2),)
    assert ordering_transform((p2, p1)) == (p2, p1)
    assert ordering_transform((p2, p1, '+{}'.format(p2))) == (p2, p1, p2)


@pytest.mark.parametrize('prop', FAIL_PROPS)
def test_ordering_property_fail(prop):
    with pytest.raises(LarkError):
        ordering_transform(prop)


# Temporary is here
def test_select_ok():
    RQLParser.parse('select(prop)')