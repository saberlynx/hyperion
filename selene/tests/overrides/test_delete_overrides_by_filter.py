# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class DeleteOverridesByFilterTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                deleteOverridesByFilter(filterString: "name~Clone") {
                   ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delete_filtered_overrides(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        mock_gmp.mock_response(
            'get_overrides',
            f'''
            <get_overrides_response status="200" status_text="OK">
                <override id="{id1}">
                    <text>Foo Clone 1</text>
                </override>
                <override id="{id2}">
                    <text>Foo Clone 2</text>
                </override>
            </get_overrides_response>
            ''',
        )

        response = self.query(
            '''
            mutation {
                deleteOverridesByFilter(filterString: "name~Clone") {
                   ok
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deleteOverridesByFilter']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.get_overrides.assert_called_with(
            filter='name~Clone'
        )

        mock_gmp.gmp_protocol.delete_override.assert_any_call(
            override_id=str(id1)
        )

        mock_gmp.gmp_protocol.delete_override.assert_any_call(
            override_id=str(id2)
        )
