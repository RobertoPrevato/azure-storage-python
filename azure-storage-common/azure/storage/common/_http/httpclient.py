# -------------------------------------------------------------------------
# Copyright (c) Microsoft.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
import urllib
import logging
from . import HTTPResponse
from .._serialization import _get_data_bytes_or_stream_only
logger = logging.getLogger(__name__)


class _HTTPClient(object):
    '''
    Takes the request and sends it to cloud service and returns the response.
    '''

    def __init__(self, protocol=None, session=None, timeout=None):
        '''
        :param str protocol:
            http or https.
        :param requests.Session session:
            session object created with requests library (or compatible).
        :param int timeout:
            timeout for the http request, in seconds.
        '''
        self.protocol = protocol
        self.session = session
        self.timeout = timeout

        # By default, requests adds an Accept:*/* and Accept-Encoding to the session, 
        # which causes issues with some Azure REST APIs. Removing these here gives us 
        # the flexibility to add it back on a case by case basis.
        # if 'Accept' in self.session.headers:
        #    del self.session.headers['Accept']

        # if 'Accept-Encoding' in self.session.headers:
        #    del self.session.headers['Accept-Encoding']

        self.proxies = None

    def set_proxy(self, host, port, user, password):
        '''
        Sets the proxy server host and port for the HTTP CONNECT Tunnelling.

        Note that we set the proxies directly on the request later on rather than
        using the session object as requests has a bug where session proxy is ignored
        in favor of environment proxy. So, auth will not work unless it is passed
        directly when making the request as this overrides both.

        :param str host:
            Address of the proxy. Ex: '192.168.0.100'
        :param int port:
            Port of the proxy. Ex: 6000
        :param str user:
            User for proxy authorization.
        :param str password:
            Password for proxy authorization.
        '''
        if user and password:
            proxy_string = '{}:{}@{}:{}'.format(user, password, host, port)
        else:
            proxy_string = '{}:{}'.format(host, port)

        self.proxies = {'http': 'http://{}'.format(proxy_string),
                        'https': 'https://{}'.format(proxy_string)}

    async def perform_request(self, request):
        '''
        Sends an HTTPRequest to Azure Storage and returns an HTTPResponse. If 
        the response code indicates an error, raise an HTTPError.    
        
        :param HTTPRequest request:
            The request to serialize and send.
        :return: An HTTPResponse containing the parsed HTTP response.
        :rtype: :class:`~azure.storage.common._http.HTTPResponse`
        '''
        # Verify the body is in bytes or either a file-like/stream object
        if request.body:
            request.body = _get_data_bytes_or_stream_only('request.body', request.body)

        # Construct the URI
        uri = self.protocol.lower() + '://' + request.host + request.path

        # Send the request
        method = request.method
        try:
            # in aiohttp, the query string must be an actual string (due to changes in one of its dependencies)
            query_string = urllib.parse.urlencode(request.query)

            response = await self.session.request(request.method,
                                              uri,
                                              params=query_string, # request.query,
                                              headers=request.headers,
                                              data=request.body, # or None ?
                                              timeout=self.timeout,
                                             ) # proxies=self.proxies -- apparently aiohttp can have one proxy, not many (https://docs.aiohttp.org/en/stable/client_reference.html)
        except Exception as ex:
            print(ex)
            raise

        # Parse the response
        status = response.status
        response_headers = {}
        for key, name in response.headers.items():
            response_headers[key.lower()] = name

        # TODO: lazily read the response content when necessary
        content = await response.text()

        wrap = HTTPResponse(status, response.reason, response_headers, content)
        response.close()

        return wrap
