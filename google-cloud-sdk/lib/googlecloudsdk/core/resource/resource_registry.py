# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Resource info registry."""

from googlecloudsdk.core.resource import resource_exceptions
from googlecloudsdk.core.resource import resource_info

RESOURCE_REGISTRY = {

    # cloud billing
    'cloudbilling.billingAccounts':
        resource_info.ResourceInfo(
            cache_command='billing accounts list',
            # TODO(b/22402915) Delete this when OP resource completion is
            # supported.
            bypass_cache=True,
            list_format="""
          table(
            name.basename():label=ID,
            displayName:label=NAME,
            open
          )
        """,),

    # cloud key management system
    'cloudkms.projects.locations':
        resource_info.ResourceInfo(
            bypass_cache=True,
            list_command='kms locations list --format=value(location_id)',
            list_format="""
          table(
            locationId
          )
        """,),

    # Cloud SDK client side resources

    # compute

    # This entry is needed due to a bug in the resource parser. It will be
    # removable when the new completion code lands.
    'compute.instances':
        resource_info.ResourceInfo(
            async_collection='compute.operations',
            cache_command='compute instances list',
            list_format="""
          table(
            name,
            zone.basename(),
            machineType.machine_type().basename(),
            scheduling.preemptible.yesno(yes=true, no=''),
            networkInterfaces[].networkIP.notnull().list():label=INTERNAL_IP,
            networkInterfaces[].accessConfigs[0].natIP.notnull().list()\
            :label=EXTERNAL_IP,
            status
          )
        """,),

    # container
    'container.images':
        resource_info.ResourceInfo(
            list_format="""
          table(
            name
          )
        """,),
    'container.tags':
        resource_info.ResourceInfo(
            list_format="""
          table(
            digest.slice(7:19).join(''),
            tags.list(),
            timestamp.date():optional,
            BUILD_DETAILS.buildDetails.provenance.sourceProvenance.sourceContext.context.cloudRepo.revisionId.notnull().list().slice(:8).join(''):optional:label=GIT_SHA,
            PACKAGE_VULNERABILITY.vulnerabilityDetails.severity.notnull().count().list():optional:label=VULNERABILITIES,
            IMAGE_BASIS.derivedImage.sort(distance).map().extract(baseResourceUrl).slice(:1).map().list().list().split('//').slice(1:).list().split('@').slice(:1).list():optional:label=FROM,
            BUILD_DETAILS.buildDetails.provenance.id.notnull().list():optional:label=BUILD
          )
        """,),
    'container.projects.zones.clusters':
        resource_info.ResourceInfo(
            async_collection='container.projects.zones.clusters',
            list_format="""
          table(
            name,
            zone,
            master_version():label=MASTER_VERSION,
            endpoint:label=MASTER_IP,
            nodePools[0].config.machineType,
            currentNodeVersion:label=NODE_VERSION,
            currentNodeCount:label=NUM_NODES,
            status
          )
        """,),
    'container.projects.zones.clusters.nodePools':
        resource_info.ResourceInfo(
            list_format="""
          table(
            name,
            config.machineType,
            config.diskSizeGb,
            version:label=NODE_VERSION
          )
        """,),
    'container.projects.zones.operations':
        resource_info.ResourceInfo(
            list_format="""
          table(
            name,
            operationType:label=TYPE,
            zone,
            targetLink.basename():label=TARGET,
            statusMessage,
            status
          )
        """,),

    # iam
    'iam.service_accounts':
        resource_info.ResourceInfo(
            list_command='iam service-accounts list --format=value(email)',
            bypass_cache=True,
            list_format="""
          table(
            displayName:label=NAME,
            email
          )
        """,),

    # runtime config
    'runtimeconfig.configurations':
        resource_info.ResourceInfo(
            list_format="""
          table(
            name,
            description
          )
        """,),
    'runtimeconfig.variables':
        resource_info.ResourceInfo(
            list_format="""
          table(
            name,
            updateTime.date()
          )
        """,),
    'runtimeconfig.waiters':
        resource_info.ResourceInfo(
            async_collection='runtimeconfig.waiters',
            list_format="""
          table(
            name,
            createTime.date(),
            waiter_status(),
            error.message
          )
        """,),

    # firebase test
    'test.android.devices':
        resource_info.ResourceInfo(  # Deprecated
            list_format="""
          table[box](
            id:label=DEVICE_ID,
            manufacturer:label=MAKE,
            name:label=MODEL_NAME,
            form.color(blue=VIRTUAL,yellow=PHYSICAL):label=FORM,
            format("{0:4} x {1}", screenY, screenX):label=RESOLUTION,
            supportedVersionIds.list(undefined="none"):label=OS_VERSION_IDS,
            tags.list().color(green=default,red=deprecated,yellow=preview)
          )
        """,),
    'firebase.test.android.models':
        resource_info.ResourceInfo(
            list_format="""
          table[box](
            id:label=MODEL_ID,
            manufacturer:label=MAKE,
            name:label=MODEL_NAME,
            form.color(blue=VIRTUAL,yellow=PHYSICAL):label=FORM,
            format("{0:4} x {1}", screenY, screenX):label=RESOLUTION,
            supportedVersionIds.list(undefined="none"):label=OS_VERSION_IDS,
            tags.list().color(green=default,red=deprecated,yellow=preview)
          )
        """,),
    'firebase.test.android.versions':
        resource_info.ResourceInfo(
            list_format="""
          table[box](
            id:label=OS_VERSION_ID:align=center,
            versionString:label=VERSION:align=center,
            codeName,
            apiLevel:align=center,
            releaseDate.date(format='%Y-%m-%d'):align=center,
            tags.list().color(green=default,red=deprecated,yellow=preview)
          )
        """,),
    'firebase.test.android.locales':
        resource_info.ResourceInfo(
            list_format="""
          table[box](
            id:label=LOCALE,
            name,
            region,
            tags.list().color(green=default,red=deprecated,yellow=preview)
          )
        """,),
    'firebase.test.android.run.outcomes':
        resource_info.ResourceInfo(
            async_collection='firebase.test.android.run.url',
            list_format="""
          table[box](
            outcome.color(red=Fail, green=Pass, yellow=Inconclusive),
            axis_value:label=TEST_AXIS_VALUE,
            test_details:label=TEST_DETAILS
          )
        """,),
    'firebase.test.android.run.url':
        resource_info.ResourceInfo(
            list_format="""
          value(format(
            'Final test results will be available at [{0}].', [])
          )
        """,),
    'firebase.test.network-profiles':
        resource_info.ResourceInfo(
            list_format="""
          table[box](
            id:label=PROFILE_ID,
            synthesize((rule:up, upRule),(rule:down, downRule)):
              format="table[box](
                rule,
                delay,
                packetLossRatio:label=LOSS_RATIO,
                packetDuplicationRatio:label=DUPLICATION_RATIO,
                bandwidth,
                burst
              )"
          )
        """,),

    # special IAM roles completion case
    'iam.roles':
        resource_info.ResourceInfo(
            bypass_cache=True,),

    # generic
    'default':
        resource_info.ResourceInfo(
            list_format="""
          default
        """,),
    'uri':
        resource_info.ResourceInfo(
            list_format="""
          table(
            uri():sort=1:label=""
          )
        """,),
}


def Get(collection, must_be_registered=False):
  """Returns the ResourceInfo for collection or None if not registered.

  Args:
    collection: The resource collection.
    must_be_registered: Raises exception if True, otherwise returns None.

  Raises:
    UnregisteredCollectionError: If collection is not registered and
      must_be_registered is True.

  Returns:
    The ResourceInfo for collection or an default ResourceInfo if not
      registered.
  """
  info = RESOURCE_REGISTRY.get(collection, None)
  if not info:
    if not must_be_registered:
      return resource_info.ResourceInfo()
    raise resource_exceptions.UnregisteredCollectionError(
        'Collection [{0}] is not registered.'.format(collection))
  info.collection = collection
  return info
