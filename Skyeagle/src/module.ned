//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package skyeagle;

import inet.networklayer.ipv4.RoutingTableRecorder;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;

import inet.node.aodv.AodvRouter;
import inet.node.inet.AdhocHost;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import inet.node.inet.WirelessHost;
import inet.node.wireless.AccessPoint;

import inet.physicallayer.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;

import inet.visualizer.contract.IIntegratedVisualizer;



module Provider extends AccessPoint
{
    parameters:
        @display("p=205,69");

        numWlanInterfaces = 1;
    gates:
		
    connections allowunconnected:
}

module Node extends AodvRouter
{
    parameters:
        double RE = default(0);
        bool sendMsgOnInit = default(false);
		
        numWlanInterfaces = 1;
        @display("bgb=1255.2749,741.82495");
    submodules:
        
}

module ClusterHead extends Node
{
    @display("bgb=1253.7,741.82495");
}

module ClusterMember extends Node
{
    parameters:
        sendMsgOnInit = true;
}

channel Link extends ned.DatarateChannel
{
    parameters:
        int cost = default(0);
        int SNR = default(0);

        datarate = default(100Mbps);
        delay = default(1ms);
        ber = default(0); // bit error rate (BER)
        per = default(0); // packet error rate (PER)
}

network eagle
{
    parameters:
        int numHost;

    submodules:
        visualizer: <default("IntegratedCanvasVisualizer")> like IIntegratedVisualizer if hasVisualizer() 
        {
            parameters:
                @display("p=100,400;is=s");
        }
        
        routingTableRecorder: RoutingTableRecorder 
        {
            parameters:
                @display("p=100,300;is=s");
        }
        
        configurator: Ipv4NetworkConfigurator 
        {
            parameters:
                @display("p=100,100;is=s");
        }
        
        radioMedium: Ieee80211ScalarRadioMedium 
        {
            parameters:
                @display("p=100,200;is=s");
        }

        provider: Provider;
        
        host[numHost]: Node 
        {
            parameters:
                @display("p=250,200");
        }

    connections: 
}
