# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Greenbone Networks GmbH
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

# pylint: disable=no-self-argument, no-member

import graphene

from gvm.protocols.latest import (
    CredentialType as GvmCredentialType,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)

from selene.schema.entity import EntityObjectType
from selene.schema.scanners.fields import Scanner
from selene.schema.targets.fields import Target
from selene.schema.utils import (
    get_boolean_from_element,
    get_text_from_element,
    get_subelement,
)


class CredentialType(graphene.Enum):
    class Meta:
        enum = GvmCredentialType


class AuthAlgorithm(graphene.Enum):
    class Meta:
        enum = SnmpAuthAlgorithm


class PrivacyAlgorithm(graphene.Enum):
    class Meta:
        enum = SnmpPrivacyAlgorithm


class Credential(EntityObjectType):

    login = graphene.String()

    allow_insecure = graphene.Boolean()

    credential_type = graphene.Field(CredentialType, name="type")
    auth_algorithm = graphene.Field(AuthAlgorithm)
    privacy_algorithm = graphene.Field(PrivacyAlgorithm)
    scanners = graphene.List(Scanner)
    targets = graphene.List(Target)

    def resolve_login(root, _info):
        return get_text_from_element(root, 'login')

    def resolve_allow_insecure(root, _info):
        return get_boolean_from_element(root, 'allow_insecure')

    def resolve_credential_type(root, _info):
        return get_text_from_element(root, 'type')

    def resolve_auth_algorithm(root, _info):
        return get_text_from_element(root, 'auth_algorithm')

    def resolve_privacy_algorithm(root, _info):
        privacy = get_subelement(root, 'privacy')
        return get_text_from_element(privacy, 'algorithm')

    def resolve_scanners(root, _info):
        scanners = root.find('scanners')
        if len(scanners) == 0:
            return None
        return scanners.findall('scanner')

    def resolve_targets(root, _info):
        targets = root.find('targets')
        if len(targets) == 0:
            return None
        return targets.findall('target')
