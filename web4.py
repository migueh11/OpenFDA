#Copyright [2017] [Miguel Hornero Berrío]<miguelhornero28@gmail.com>

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import http.server
import http.client
import json
import socketserver

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    OPENFDA_API_LYRICA = '?search=patient.drug.medicinalproduct:"LYRICA"&limit=10'

    def get_main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA app</title>
            </head>
            <body>
                <h1>OpenFDA CloolApp</h1>
                <form method='get' action='receivedrug'>
                    <input type='submit' value='Drug list: Send to OpenFDA'></input>
                </form>
                <form method='get' action='searchdrug'>
                    <input type='text' name='drug'></input>
                    <input type='submit' value='Drug Search: Send to OpenFDA'></input>
                </form>
                <form method='get' action='receivecompany'>
                    <input type='submit' value='List of Company numbers: Send to OpenFDA'></input>
                </form>
                <form method='get' action='searchcompany'>
                    <input type='text' name='drug'></input>
                    <input type='submit' value='Company Search: Send to OpenFDA'></input>
                </form>

            </body>
        </html>
                '''
        return html
    def get_all_drugs(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+drug+'&limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        #event = events['results'][0]['patient']['drug']
        return events

    def get_medicinalproduct(self,company):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb:'+company+'&limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        #event = events['results'][0]['patient']['drug']
        return events

    def get_event(self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        #event = events['results'][0]['patient']['drug']
        return events

    def get_drug(self, events):
        medicamentos=[]
        for event in events['results']:
            medicamentos+=[event['patient']['drug'][0]['medicinalproduct']]

        return medicamentos
    def get_com_num(self, events):
        com_num=[]
        for event in events['results']:
            com_num+=[event['companynumb']]
        return com_num

    def drug_page(self,medicamentos):
        s=''
        for drug in medicamentos:
            s += "<li>"+drug+"</li>"
        html='''
        <html>
            <head></head>
                <body>
                    <ul>
                        %s
                    </ul>
                </body>
        </html>''' %(s)
        return html

    def do_GET(self):

        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        if self.path == '/' :
            html = self.get_main_page()
            self.wfile.write(bytes(html,'utf8'))
        elif self.path == '/receivedrug?':
            events = self.get_event()
            medicamentos = self.get_drug(events)
            html = self.drug_page(medicamentos)
            self.wfile.write(bytes(html,'utf8'))
        elif self.path == '/receivecompany?':
            events = self.get_event()
            com_num=self.get_com_num(events)
            html=self.drug_page(com_num)
            self.wfile.write(bytes(html,'utf8'))

        elif 'searchdrug' in self.path:
            drug=self.path.split('=')[1]
            events = self.get_all_drugs(drug)
            com_num = self.get_com_num(events)
            html = self.drug_page(com_num)
            self.wfile.write(bytes(html,'utf8'))

        elif 'searchcompany' in self.path:
            com_num=self.path.split('=')[1]
            events = self.get_medicinalproduct(com_num)
            medicinalproduct= self.get_drug(events)
            html = self.drug_page(medicinalproduct)
            self.wfile.write(bytes(html,'utf8'))

        return
