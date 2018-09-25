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

package sky;

import inet.node.inet.AdhocHost;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import inet.node.inet.WirelessHost;
import inet.node.inet.INetworkNode;
import inet.node.wireless.AccessPoint;


import inet.visualizer.contract.IIntegratedVisualizer;
import inet.visualizer.integrated.IntegratedCanvasVisualizer;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;

import inet.physicallayer.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;
import inet.physicallayer.contract.packetlevel.IRadioMedium;

//
// TODO auto-generated type
//

module Node extends AdhocHost 
{
    parameters:
        double RE = default(0);
        bool sendMsgOnInit = default(false);
        @display("i=block/routing");
    gates:
        inout gate[];
    connections allowunconnected:
}


module Provider extends Node 
{
    parameters:
        sendMsgOnInit = false;      
        @display("i=block/routing");

}

module UAV extends Node
{
    parameters:
        sendMsgOnInit = true;
        
        @display("i=abstract/router_s");
        
        @signal[arrival](type="long");
        @statistic[hopCount](title="hop count"; source="arrival"; record=vector,stats; interpolationmode=none);
        
        
      	@figure[description](type=text; pos=5,20; font=,,bold; 
        	text="Random routing example - displaying last hop count");
        @figure[lasthopcount](type=text; pos=5,35; text="last hopCount: N/A");        
}

channel Link extends ned.DatarateChannel 
{
    parameters:
        int cost = default(0);
        int SNR = default(0);
        
        datarate = default(1024bps);
        delay = default(5ms);
        ber = default(0); // bit error rate (BER)
        per = default(0); // packet error rate (PER)
}

network eagle 
{
    parameters:
        @display("bgb=650,500;bgg=100,1,grey95");
        @figure[title](type=label; pos=0,-1; anchor=sw; color=darkblue);

        @figure[rcvdPkText](type=indicatorText; pos=380,20; anchor=w; font=,18; textFormat="packets received: %g"; initialValue=0);
        @statistic[packetReceived](source=hostB.app[0].packetReceived; record=figure(count); targetFigure=rcvdPkText);

    submodules:
        visualizer: <default("IntegratedCanvasVisualizer")> like IIntegratedVisualizer if hasVisualizer() {
            @display("p=580,125");
        }
        configurator: Ipv4NetworkConfigurator {
            @display("p=580,200");
        }
        radioMedium: <default("UnitDiskRadioMedium")> like IRadioMedium {
            @display("p=580,275");
        }
        hostA: <default("WirelessHost")> like INetworkNode {
            @display("p=50,325");
        }
        hostB: <default("WirelessHost")> like INetworkNode {
            @display("p=450,325");
        }
}