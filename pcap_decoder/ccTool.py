import sys
import re
import matplotlib.pyplot as plt
import zipfile
import argparse
import tempfile
import os
import math

def Usage():
    print("Usage <in> <out> [ports]")
    sys.exit(0)

def readConversations(infile):
    ue2flow = {}
    flow2ue = {}
    if infile is None:
        return (ue2flow, flow2ue)

    convPattern = re.compile("(.*?)  <-> (.*?) (.*)")
    with open(infile) as f:
        for line in f:
            m = convPattern.match(line)
            if m:
                src = m[1]
                dst = m[2]
                (ue_ip, ue_port) = src.split(':')
                (dst_ip, dst_port) = dst.split(':')
                print("{} -> {}".format(ue_ip, dst_ip))
                if ue_ip not in ue2flow:
                    ue2flow[ue_ip] = []

                flow = "{}-{}".format(ue_port, dst_port)
                ue2flow[ue_ip].append(flow)
                flow2ue[flow] = ue_ip
    return (ue2flow, flow2ue)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile", help="input")
parser.add_argument("-o", "--outfile", help="output")
parser.add_argument("-p", "--ports", nargs='+', help='ports to filter')
parser.add_argument("-s", "--summary", action="store_true", help='provide a flow summary')
parser.add_argument("-c", "--conversations", help="TCP conversations extracted by wireshark")
parser.add_argument("-tmax", "--max_time", help="time limit max", type=int)
parser.add_argument("-tmin", "--min_time", help="time limit min", type=int, default=0)
parser.add_argument("-ver", "--version", help="version", default='latest')
parser.add_argument("-perms", "--perms", help="per ms output", action="store_true")
parser.add_argument("-csv", "--csv", help="csv output", action="store_true")
parser.add_argument("-l", "--cwnd_limit", help="cwnd limit", type=int, default=3000)
parser.add_argument("-a", "--perflow", help="perflow", action="store_true")
parser.add_argument("-tpmin", "--min_throughput", help="min. throughput", type=int, default=0)
args = parser.parse_args()

#if len(sys.argv) < 4:
#    Usage()

#infile = args.infile
#outfile = sys.argv[2]

print(args)
 
if args.infile is None:
    Usage()

(ue2flow, flow2ue) = readConversations(args.conversations)
for ue in ue2flow.keys():
    print("{} : {}".format(ue, ue2flow[ue]))
for flow in flow2ue.keys():
    print("{} : {}".format(flow, flow2ue[flow]))

print("ports = {}".format(args.ports))
if args.ports:
    p = re.compile("(.*?)(" + "|".join(port + "->" for port in args.ports) + ")")
else:
    print("Matching all ports")
    p = re.compile("(.*?)(.*?->)")
print(p)

ignorePattern = re.compile("(.*?)(TX_START|MID_FLOW_INFO|TXUE|RXUE|TXSE|RXSE)")
# 12:00:23,32714,0,44036->80,CC:0x2ba36465e030,686512984,6366342,1448,101448,104704,0,29,1,200,0,4194304,1448,0,0,0,0,0,37648,0,3197383343,3197462983,5204.020441,0,0,0,0,0,0,0,0,79640,21808,0x200,0,0,0,0,0,5203.989447,10136,27512,0.030994,0.030028,0,1448,26064,0,0,30000,686512918,0,28,2,10819,2,10819,2,10819,2,30408,0,0,0,0,0,0,0,0,10819,0,0,0,0,0,0,0,0,739,739,0,0,0,1,0,10819,5204020276,18,0,6,2,0,0,0,0,0,0
CC_pattern = re.compile("(.*?);(RS:.*?);(OPT:.*)")

flows = {}
events = {}
count = 0
t0 = -1
tmax = 0
dataKeys = "logTimeStamp,logId,rel_time_ms,remote->local,log_id,timestamp_ms,pacing_rate,MSS,cwnd,ssthresh,snd_wnd,srtt,rttVar,rto,rto_boff,tx_fifo_size,bytes_acked,snd_space,rxt_delivered,prr_delivered,rcv_dupacks,dupacks_in,delivered,appLimited,sndUna,maxSndNxt,delivered_time,caState,sack.last_bytes.delivered,sack.rxt_sacked,sack.sacked_bytes,sack.last_sacked_bytes,sack.last_lost_bytes,sack.lost_bytes,snd_rxt_bytes,tcp_flight_size,cc_space,flags,fast_retrans_count,rto_count,segs_retrans,bytes_retrans,sack_reneging,rs.prior_time,rs.prior_delivered,rs.delivered,rs.interval_time,rs.rtt_time,rs.last_lost,rs.lost,rs.acked_and_sacked,rs.tx_in_flight,rs.isAppLimited,rs.isRetrans,min_rtt_us,min_rtt_timestamp_ms,probe_rtt_done_stamp_ms,srtt_rttvar,bw[0].t,bw[0].v,bw[1].t,bw[1].v,bw[2].t,bw[2].v,rtt_count,next_rtt_delivered,cycle_mstamp_ms,current_mode,prev_ca_state,packet_consrv_mode,restore_cwnd,round_start,max_rtt,idle_restart,max_bw,probe_rtt_round_done,is_long_term_sampling,lt_rtt_count,use_long_term_bw,long_term_bw,long_term_last_delivered,long_term_last_mstamp,long_term_last_lost,tcp_pacing_gain,cwnd_gain,full_bw_reached,full_bw_cnt,cycle_index,has_seen_rtt,prior_cwnd,full_bw,ack_epoch_mstamp,extra_acked[0],extra_acked[1],ack_epoch_acked,extra_acked_win_rtts,extra_acked_win_idx,prior_in_flight,rtt_congested,loss_rate_exceeded,high_rtt_exceeded,v2_enabled,dyn_pacing_boost_active,max_bw_short,max_bw_long,loss_rate_exceeded_cnt,loss_timestamp_ms,loss_thresh_last_delivered,loss_thresh_last_lost,inflight_hi,target_cwnd".split(",")

#
EVENT = "log_id"
FLOW = "remote->local"
TIME = "timestamp_ms"
RATE = "pacing_rate"
CWND = "cwnd"
SRTT = "srtt"
MAX_RTT = "max_rtt"
FLAGS = "flags"
DELIVERED = "delivered"
CA_STATE = "caState"
INFLIGHT = "tcp_flight_size"
APP_LIMITED = "appLimited"
RS_RTT = "rs.rtt_time"
RS_DELIVERED = "rs.delivered"
RS_INTERVAL = "rs.interval_time"
RS_LOST = "rs.lost"
RS_TX_IN_FLIGHT = "rs.tx_in_flight"
OPT_MIN_RTT = "min_rtt_us"
OPT_RTT_COUNT = "rtt_count"
LT_RTT_COUNT = "lt_rtt_count"
OPT_MODE = "current_mode"
OPT_PREV_CA_STATE = "prev_ca_state"
OPT_PKT_CONSERV_MODE = "packet_consrv_mode"
OPT_RESTORE_CWND = "restore_cwnd"
OPT_MAX_BW = "max_bw"
OPT_USE_LT_BW = "use_long_term_bw"
OPT_EST_BW = "OPT_est_bw"
OPT_FULL_BW_CNT = "full_bw_cnt"
OPT_FULL_BW = "full_bw"
OPT_FULL_BW_REACHED = "full_bw_reached"
OPT_CWND_GAIN = "cwnd_gain"
OPT_PRIOR_CWND = "prior_cwnd"
OPT_PACING_GAIN = "tcp_pacing_gain"
LOSS_RATE_EXCEEDED_CNT = "loss_rate_exceeded_cnt"
LOSS_THRESH_LAST_DELIVERED = "loss_thresh_last_delivered"
LOSS_RATE_EXCEEDED = "loss_rate_exceeded"
HIGH_RTT_EXCEEDED = "high_rtt_exceeded"
INFLIGHT_HI = "inflight_hi"
TARGET_CWND = "target_cwnd"
BW_MAX0="bw[0].v"
BW_MAX1="bw[1].v"
BW_MAX2="bw[2].v"
extractKeys = [TIME, EVENT, FLOW, RATE, CWND, SRTT, DELIVERED, CA_STATE, INFLIGHT, FLAGS, RS_RTT, APP_LIMITED, OPT_MIN_RTT, OPT_RTT_COUNT, OPT_MODE, OPT_PKT_CONSERV_MODE, OPT_RESTORE_CWND, OPT_MAX_BW, OPT_USE_LT_BW, RS_DELIVERED, RS_INTERVAL, RS_LOST, RS_TX_IN_FLIGHT, OPT_FULL_BW_CNT, OPT_FULL_BW, OPT_FULL_BW_REACHED, OPT_CWND_GAIN, OPT_PACING_GAIN, OPT_PREV_CA_STATE, LOSS_RATE_EXCEEDED_CNT, LOSS_THRESH_LAST_DELIVERED, LT_RTT_COUNT, OPT_PRIOR_CWND, LOSS_RATE_EXCEEDED, HIGH_RTT_EXCEEDED, BW_MAX0, BW_MAX1, BW_MAX2, MAX_RTT, INFLIGHT_HI, TARGET_CWND ]

extractIndices = {}
for key in extractKeys:
    if key in dataKeys:
        print("{} : {}".format(key, dataKeys.index(key)))
        idx = dataKeys.index(key)
        extractIndices[key] = idx
    else:
        print("{} not found".format(key))
        sys.exit(0)

BDP = "bdp"
RS = "RS"
OPT_CWND_GAIN_CALC = "OPT_cwnd_gain_calc"
PROBE_BW_START_TIME = "probe_bw_start_time"
OPT_BDP = "OPT_bdp"
RS_RATE_EST = "rs.rate_est"
RS_LOST_PERCENT = "rs_lost_percent"
TIME_DELTA = "t delta"
EVENT_TYPE = "event"
ESTIMATED_THROUGHPUT = "est_throughput"
derivedKeys = [ OPT_CWND_GAIN_CALC, PROBE_BW_START_TIME, OPT_BDP, RS_RATE_EST, TIME_DELTA, RS_LOST_PERCENT, EVENT_TYPE, ESTIMATED_THROUGHPUT ]

flowKeys = extractKeys + derivedKeys

print(flowKeys)


graphs = {
    EVENT: { "y":EVENT_TYPE, "ylabel":"Event", "enabled":False},
    RATE : { "y":RATE, "ylabel":"Pacing Rate (Mbps)", "enabled":True},
    CWND : { "y":CWND, "ylabel":"CWND (kbytes)", "ylim":[0, 2000], "enabled":True, "y2": OPT_PRIOR_CWND, "y2label": "Prior CWND", "y2lim":[0, 2000]},
    OPT_CWND_GAIN: { "y":OPT_CWND_GAIN, "ylabel":"CWND gain", "enabled":True, "y2": LOSS_RATE_EXCEEDED_CNT, "y2label": "Loss rate exceeded"},
    "OPT_CWND_RED" : { "y2":OPT_CWND_GAIN, "y2label":"CWND gain", "enabled":False, "y": LOSS_RATE_EXCEEDED_CNT, "ylabel": "Loss Rate Exceeded"},
    INFLIGHT : { "y":INFLIGHT, "ylabel":"inflight (kbytes)", "enabled":True},
    DELIVERED : { "y":DELIVERED, "ylabel":"bytes (kbytes)", "enabled":True, "y2": LOSS_THRESH_LAST_DELIVERED, "y2label":LOSS_THRESH_LAST_DELIVERED},
    SRTT : { "y":SRTT, "ylabel":"srtt (ms)", "enabled":True},
    APP_LIMITED : { "y":APP_LIMITED, "ylabel":"App. Limited", "enabled":True},
    OPT_RTT_COUNT : { "y":OPT_RTT_COUNT, "ylabel":"RTT Count", "enabled":False},
    LT_RTT_COUNT : { "y":LT_RTT_COUNT, "ylabel":"LT RTT Count", "enabled":False},
    OPT_MODE : { "y":OPT_MODE, "ylabel":"MODE", "enabled":True},
    OPT_PKT_CONSERV_MODE : { "y":OPT_PKT_CONSERV_MODE, "ylabel":"Packet conservation mode", "enabled":False},
    "OPT_CWND_AND_PKT_CONSERV_MODE" : { "y":CWND, "ylabel":"CWND (kbytes)", "enabled":False, "y2":OPT_PKT_CONSERV_MODE, "y2label":"Packet conservation mode" },
    "OPT_RESTORE_CWND_AND_PKT_CONSERV_MODE" : { "y":OPT_RESTORE_CWND, "ylabel":"RESTORE_CWND", "enabled":False, "y2":OPT_PKT_CONSERV_MODE, "y2label":"Packet conservation mode" },
    OPT_MIN_RTT : { "y":OPT_MIN_RTT, "ylabel":"min rtt", "enabled":False},
    OPT_MAX_BW : { "y":OPT_MAX_BW, "ylabel":"max bw", "enabled":True},
    OPT_USE_LT_BW : { "y":OPT_USE_LT_BW, "ylabel":"use lt bw", "enabled":False},
    "Maximum vs Long-term BW" : { "y":OPT_USE_LT_BW, "ylabel":"use lt bw", "enabled":False, "y2":OPT_MAX_BW, "y2label":"max bw"},
    OPT_EST_BW : { "y":OPT_EST_BW, "ylabel":"est bw", "enabled":False},
    RS_INTERVAL: { "y":RS_INTERVAL, "ylabel":"RS interval", "enabled":False},
    RS_DELIVERED : { "y":RS_DELIVERED, "ylabel":"RS delivered", "enabled":False},
    RS_RATE_EST : { "y":RS_RATE_EST, "ylabel":"RS est bw", "enabled":True},
    BW_MAX0: { "y":BW_MAX0, "ylabel":"bw max0", "enabled":True},
    BW_MAX1: { "y":BW_MAX1, "ylabel":"bw max1", "enabled":False},
    BW_MAX2: { "y":BW_MAX2, "ylabel":"bw max2", "enabled":False},
    RS_TX_IN_FLIGHT : { "y":RS_TX_IN_FLIGHT, "ylabel":"rs in flight", "enabled":False},
    RS_LOST : { "y":RS_LOST, "ylabel":"RS lost", "enabled":True, "y2":RS_LOST_PERCENT, "y2label":"rs lost percent", "y2lim":(0,10)},
    LOSS_RATE_EXCEEDED : { "y":LOSS_RATE_EXCEEDED, "ylabel":"Loss rate exceeded", "enabled":False, "y2":HIGH_RTT_EXCEEDED, "y2label":"High RTT exceeded", "y2lim":(0,5)},
    HIGH_RTT_EXCEEDED : { "y":HIGH_RTT_EXCEEDED, "ylabel":"High RTT exceeded", "enabled": False },
    "Pacing gain vs rate" : { "y2":RS_RATE_EST, "y2label":"RS est bw", "enabled":True, "y": OPT_PACING_GAIN, "ylabel": "Pacing Gain" },
    "Pacing rate vs max" : { "y2":OPT_MAX_BW, "y2label":"Max. bw", "enabled":False, "y": RATE, "ylabel": "Pacing Gain" },
    "Pacing gain vs lost" : { "y2":RS_LOST, "y2label":"RS lost", "enabled":False, "y": RATE, "ylabel": "Pacing Gain" },
    "Delivery vs rate" : { "y12":RS_RATE_EST, "y12label":"RS est bw", "enabled":False, "y": RATE, "ylabel": "Pacing Rate (Mbps)" },
    "srtt vs interval" : { "y12":RS_INTERVAL, "y12label":"RS interval", "enabled":False, "y": SRTT, "ylabel": "srtt" },
    "RATE_SAMPLE" : { "y2":RS_DELIVERED, "y2label":"RS Delivered", "enabled":False, "y":RS_INTERVAL, "ylabel":"RS Interval"},
    OPT_FULL_BW_CNT : { "y":OPT_FULL_BW_CNT, "ylabel":"full bw", "enabled":False, "y2":OPT_FULL_BW, "y2label":"full bw"},
    OPT_FULL_BW : { "y":OPT_FULL_BW, "ylabel":"full bw", "enabled":False},
    OPT_FULL_BW_REACHED : { "y":OPT_FULL_BW_REACHED, "ylabel":"full bw", "enabled":False},
    OPT_PACING_GAIN : { "y":OPT_PACING_GAIN, "ylabel":"Pacing gain", "enabled":False},
    OPT_CWND_GAIN_CALC : { "y":OPT_CWND_GAIN_CALC, "ylabel":"CWND gain calc", "enabled":False},
    OPT_BDP : { "y" : OPT_BDP, "ylabel": "BDP", "enabled": False },
    "CA_STATE" : {"y" : CA_STATE, "ylabel": "ca_state", "y2": OPT_PREV_CA_STATE, "y2label": "prev_ca_state", "enabled": False},
    "FLAGS" : {"y" : CA_STATE, "ylabel": "ca_state", "y2": FLAGS, "y2label": "flags", "enabled": False},
    "TIME DELTA" : {"y" : TIME_DELTA, "ylabel": "Time delta", "enabled": False},
    "MAX_RTT" : {"y" : MAX_RTT, "ylabel": "Max. rtt", "enabled": False},
    "TARGET_CWND" : {"y" : TARGET_CWND, "ylabel": "Target CWND", "enabled": False}
}
enabledGraphs = [ graph for graph in graphs.keys() if graphs[graph]["enabled"] ]
print("enabled graphs {}".format(enabledGraphs))

def vpp_time_to_us(vpp_time):
    return int( (vpp_time + 0.0000005) * 1e6 )

class ProbeBWSample:
    t = 0
    srtt = 0
    inflight = 0
    cwnd = 0
    def __init__( self, t=0, srtt=0, inflight=0, cwnd=0 ):
        self.t = t
        self.srtt = srtt
        self.inflight = inflight
        self.cwnd = cwnd

class PerMsPerFlowData:
    inflight = 0
    rate = 0
    pacing_rate = 0

class PerMsData:
    t = 0
    count = 0
    rtt = 0
    inflight = 0
    active = 0
    rate = 0
    pacing_rate = 0
    flows = {}
    def __init__(self, t):
        self.t = t
        self.count = 0
        self.rtt = 0
        self.inflight = 0
        self.active = 0
        self.rate = 0
        self.pacing_rate = 0
        self.flows = {}
per_ms = []
per_ms_range = [0, 50]
per_ms_data = PerMsData(per_ms_range[0])
per_ms.append(per_ms_data)

print(per_ms_data)

with open(args.infile) as f:
    activeFlows = 0
    for line in f:
        if ignorePattern.match(line):
            continue

        m = p.match(line)
        if m:
            line = line.strip()
            data = line.split(',')

            #key = data[0].split(' ')[-1].split('-')
            #flowId = key[0] 
            flowId = data[ extractIndices[FLOW] ].replace('>', '')
            event = data[ extractIndices[EVENT] ].split(':')[0] # data[1].split(':')[0]

            if event == "CC" or event == "CC-CONG" or event == "CONGESTION":

                flow = {}
                if flowId not in flows:
                    print("Adding flow {} ".format(flowId))
                    flow[TIME] = []
                    for flowKey in flowKeys:
                        flow[flowKey] = []
                    flow[PROBE_BW_START_TIME] = 0

                    flows[flowId] = flow
                    activeFlows += 1
                else:
                    flow = flows[flowId]

           
                if event == "CC":
                    flow[EVENT_TYPE].append(1)
                elif event == "CC-CONG":
                    flow[EVENT_TYPE].append(2)
                else:
                    flow[EVENT_TYPE].append(3)
 
                t = int(data[ extractIndices[TIME] ])
                
                if t0 == -1:
                    t0 = t
                tmax = t

                t = t - t0
                #print(opt)

                if t >= per_ms_range[1]:
                    inc = per_ms_range[1] - per_ms_range[0]
                    per_ms_range[0] = per_ms_range[1]
                    per_ms_range[1] += inc
                    per_ms_data = PerMsData(per_ms_range[0])
                    per_ms.append(per_ms_data)
                per_ms_data.count += 1
                per_ms_data.active = activeFlows

                per_ms_per_flow = None
                if flowId not in per_ms_data.flows:
                    per_ms_per_flow = PerMsPerFlowData()
                    per_ms_data.flows[flowId] = per_ms_per_flow
                else:
                    per_ms_per_flow = per_ms_data.flows[flowId]

                count+=1
                #print("{},{}".format(flowId, ",".join(flowEvent)))
                
                timeDelta = flow[TIME][-1] - t if (len(flow[TIME]) > 1) else 0
                flow[TIME].append(t)
                flow[TIME_DELTA].append(timeDelta)

                #print(len(data))
                #print(data)

                srtt = int( data[ extractIndices[SRTT] ] )
                rate = int( data[ extractIndices[RATE] ] ) * 8 / 1000000
                flow[RATE].append(rate)

                curr_pacing_rate = per_ms_per_flow.pacing_rate
                if rate > curr_pacing_rate:
                    per_ms_per_flow.pacing_rate = rate
                    per_ms_data.pacing_rate += rate - curr_pacing_rate
                flow[CWND].append(int( data[ extractIndices[CWND] ] ) / 1000)
                flow[OPT_PRIOR_CWND].append(int( data[ extractIndices[OPT_PRIOR_CWND] ] ) / 1000)

                if len(data) > extractIndices[LOSS_RATE_EXCEEDED_CNT]:
                    exceeded_cnt = data[ extractIndices[LOSS_RATE_EXCEEDED_CNT] ].strip()
                    if len(exceeded_cnt) > 0:
                        flow[LOSS_RATE_EXCEEDED_CNT].append( int(exceeded_cnt) )
                    else:
                        flow[LOSS_RATE_EXCEEDED_CNT].append(0)
                else:
                    flow[LOSS_RATE_EXCEEDED_CNT].append(0)

                if len(data) > extractIndices[LOSS_THRESH_LAST_DELIVERED]:
                    last = data[ extractIndices[LOSS_THRESH_LAST_DELIVERED] ].strip()
                    if len(last) > 0:
                       flow[LOSS_THRESH_LAST_DELIVERED].append( int(last) / 1000 )
                    else:
                       flow[LOSS_THRESH_LAST_DELIVERED].append(0)
                else:
                    flow[LOSS_THRESH_LAST_DELIVERED].append(0)

                inflight = int( data[ extractIndices[INFLIGHT] ] ) / 1000
                flow[INFLIGHT].append(inflight)
                flow[SRTT].append(srtt)

                if srtt > per_ms_data.rtt:
                    per_ms_data.rtt = srtt
                curr_inflight = per_ms_per_flow.inflight
                if inflight > curr_inflight:
                    per_ms_per_flow.inflight = inflight
                    per_ms_data.inflight += inflight - curr_inflight
                
                flow[MAX_RTT].append( int(data[extractIndices[MAX_RTT] ]))
                flags = int(data[ extractIndices[FLAGS]], 16) & 0x0C # recovery / fast recovery
                flow[FLAGS].append(flags)
                flow[CA_STATE].append(int(data[ extractIndices[ CA_STATE] ]))
                flow[DELIVERED].append(int(data[ extractIndices[ DELIVERED] ]) / 1000)
                flow[APP_LIMITED].append(int(data[ extractIndices[ APP_LIMITED] ]))
                flow[BW_MAX0].append(int(data[ extractIndices[BW_MAX0] ]))
                flow[BW_MAX1].append(int(data[ extractIndices[BW_MAX1] ]))
                flow[BW_MAX2].append(int(data[ extractIndices[BW_MAX2] ]))
                if len(data) > extractIndices[LOSS_RATE_EXCEEDED]:
                    loss_rate_ex = data[ extractIndices[LOSS_RATE_EXCEEDED] ]
                    if len(loss_rate_ex) > 0:
                        flow[LOSS_RATE_EXCEEDED].append(int(loss_rate_ex))
                    else:
                        flow[LOSS_RATE_EXCEEDED].append(0)
                else:
                    flow[LOSS_RATE_EXCEEDED].append(0)

                if len(data) > extractIndices[HIGH_RTT_EXCEEDED]:
                    high_rtt_exceeded = data[ extractIndices[HIGH_RTT_EXCEEDED] ]
                    if len(high_rtt_exceeded) > 0:
                        flow[HIGH_RTT_EXCEEDED].append(int(high_rtt_exceeded))
                    else:
                        flow[HIGH_RTT_EXCEEDED].append(0)
                else:
                    flow[HIGH_RTT_EXCEEDED].append(0)

                #flow[BDP].append( (1000 * int(data[CC_CWND])) / (int(data[CC_RATE]) * srtt) )

                mode = int( data[ extractIndices[ OPT_MODE ] ] )
                if mode == 2 and flow[PROBE_BW_START_TIME] == 0:
                    flow[PROBE_BW_START_TIME] = len(flow[TIME]) - 1

                flow[OPT_MODE].append( mode )
                flow[OPT_RTT_COUNT].append( int( data[ extractIndices[ OPT_RTT_COUNT] ] ))
                flow[LT_RTT_COUNT].append( int( data[ extractIndices[ LT_RTT_COUNT] ] ))

                flow[OPT_PKT_CONSERV_MODE].append(int( data[ extractIndices[ OPT_PKT_CONSERV_MODE ] ] ) )
                flow[OPT_RESTORE_CWND].append(int( data[ extractIndices [OPT_RESTORE_CWND] ] ) )

                minRtt = int( data[ extractIndices[ OPT_MIN_RTT ] ] )
                #print("{} {}".format( opt[OPT_min_rtt_idx], minRtt) )
                flow[OPT_MIN_RTT].append( minRtt )

                #print("{} {}".format(minRtt, mode))
                flow[OPT_MAX_BW].append( int( data[ extractIndices[ OPT_MAX_BW ] ] ) )
                flow[OPT_USE_LT_BW].append( int( data[ extractIndices[ OPT_USE_LT_BW ] ] ) )

                #estBw = int( data[ extractIndices[ [OPT_est_bw_idx])
                #flow[OPT_EST_BW].append( estBw )

                flow[OPT_FULL_BW_CNT].append( int( data[ extractIndices[ OPT_FULL_BW_CNT] ]) )
                flow[OPT_FULL_BW_REACHED].append( int( data[ extractIndices[ OPT_FULL_BW_REACHED] ]) )
                full_bw = data[ extractIndices[ OPT_FULL_BW ] ]
                flow[OPT_FULL_BW].append( int( full_bw ) if len(full_bw) > 0 else 0 )

                flow[OPT_CWND_GAIN].append( int( data[ extractIndices[ OPT_CWND_GAIN ] ] ) )
                flow[OPT_PACING_GAIN].append( int( data[ extractIndices[ OPT_PACING_GAIN ] ] ) / 256 )
                flow[OPT_PREV_CA_STATE].append(int( data[ extractIndices[ OPT_PREV_CA_STATE ] ] ))

                flow[OPT_CWND_GAIN_CALC].append( float(srtt * 1000 ) / float(minRtt) if minRtt > 0 else 0 )

                rsInterval = vpp_time_to_us( float( data[ extractIndices[RS_INTERVAL] ] ) ) / 1000
                rsDelivered = float( data[ extractIndices[ RS_DELIVERED ] ])

                mss = 1460
                BW_UNIT = 16777216
                rateEstimate = 0
                if(rsInterval > 0):
                    rateEstimate = int( 1000 * rsDelivered * 8 /  rsInterval ) / 1000000 #int (BW_UNIT * rsDelivered / rsInterval / mss ) / 1024 / 1024

                #print("{}".format(rateEstimate / rate ))
                #print("{} {} {} {} ".format(rateSample[RS_delivered_idx], rateSample[RS_interval_idx], estimate, int( opt[OPT_est_bw_idx])))
                #if estBw > 0 and rateEstimate > 0:
                #    deliveryRate = (int(data[CC_RATE]) * 8 / 1000000 )
                flow[RS_DELIVERED].append( rsDelivered )
                flow[RS_INTERVAL].append( rsInterval )
                flow[RS_RATE_EST].append( rateEstimate )

                curr_rate_est = per_ms_per_flow.rate
                if rateEstimate > curr_rate_est:
                    per_ms_per_flow.rate = rateEstimate
                    per_ms_data.rate += rateEstimate - curr_rate_est
                
                rs_lost = int(data[ extractIndices[ RS_LOST ] ])
                flow[RS_LOST].append( rs_lost )
                rs_tx_in_flight = int( data[ extractIndices[ RS_TX_IN_FLIGHT ] ])
                flow[RS_TX_IN_FLIGHT].append( rs_tx_in_flight )
                if rs_tx_in_flight > 0 and rs_lost > 0:
                    #print("{} {}".format(rs_lost, rs_tx_in_flight))
                    flow[RS_LOST_PERCENT].append( rs_lost * 100 / rs_tx_in_flight )
                else:
                    flow[RS_LOST_PERCENT].append( 0 )
                #print("{}".format( rateSample[RS_lost_idx] ))
                #print("{:.4f}".format(rateEstimate/rate))
                #flow[OPT_BDP].append( estBw * minRtt / 1000000 )
                #if(minRtt != 0 and estBw != 0):
                #    print("{} {} {} {} {} {}".format(rateEstimate, estBw, minRtt, estBw * minRtt / 1000000, int(data[CC_CWND]), int(data[CC_CWND]) / (estBw * minRtt / 1000000)))

                if len(data) > extractIndices[INFLIGHT_HI]:
                    inflight_hi = data[ extractIndices[ INFLIGHT_HI ] ]
                    if len(inflight_hi) and not inflight_hi == "4294967295":
                        flow[INFLIGHT_HI].append( int(inflight_hi) )
                    else:
                        flow[INFLIGHT_HI].append( 0 )
                else:
                    flow[INFLIGHT_HI].append( 0 )

                if len(data) > extractIndices[TARGET_CWND]:
                    target_cwnd = data[ extractIndices[ TARGET_CWND ] ]
                    if len(target_cwnd):
                        flow[TARGET_CWND].append( int(target_cwnd) )
                    else:
                        flow[TARGET_CWND].append( 0 )
                else:
                    flow[TARGET_CWND].append( 0 )

            if args.max_time != None and (tmax-t0) > args.max_time:
                args.max_time = None
                break

if args.min_throughput > 0:
    for flowId in sorted(flows.keys()):
        flow = flows[flowId]
        t = flow[TIME]
        dur = t[-1] - t[0]
        size = int(flow[DELIVERED][-1] - flow[DELIVERED][0])
        tput = 0
        if dur > 0:
            tput = int((size * 8 )/ dur)  # converting to mbps (kbytes / ms )


        if tput >= args.min_throughput:
            flow[ESTIMATED_THROUGHPUT] = tput
        else:
            print("removing flow {}".format(flowId))
# shaligram           del flows[flowId]

        

def summaryString(flowId, flow, ue = "-"):
    t = flow[TIME]
    dur = t[-1] - t[0]
    size = int(flow[DELIVERED][-1] - flow[DELIVERED][0])
    tput = 0
    if dur > 0:
        tput = int((size * 8 )/ dur)  # converting to mbps (kbytes / ms )

    probe_bw_start = flow[PROBE_BW_START_TIME]
    return "{} flow {:12} samples {:5}  start {:8}  dur {:8}  kbytes {:8}  mbps {:4}  probe_bw {:4} ({:4})".format(ue, flowId, len(t), t[0], dur, size, tput, probe_bw_start, t[probe_bw_start])

class TimeSeriesTrend:
    def __init__(self):
        self.s = 5
        self.l = 20
        self.last_short = []
        self.last_long = []

    def add(self, v):
        self.last_long.append(v)
        self.last_short.append(v)
        if (len(self.last_short) > self.s):
            self.last_short = self.last_short[1:]
        if (len(self.last_long) > self.l):
            self.last_long = self.last_long[1:]

    def toString(self):
        return "{:.3f}    {:.3f}".format( self.short_average(), self.long_average() )

    def short_average(self):
        return sum(self.last_short) / len(self.last_short)

    def long_average(self):
        return sum(self.last_long) / len(self.last_long)

class EWMATrend:
    def __init__(self):
        self.s = 5
        self.l = 20
        self.short_ewma = 0
        self.long_ewma = 0
        self.smoothing = 2
        self.count = 0

    def add(self, v):
        self.short_ewma = v * (self.smoothing / (1 + self.s) ) + self.short_ewma * ( 1 - ( self.smoothing / (1 + self.s) ) )
        self.long_ewma = v * (self.smoothing / (1 + self.l) ) + self.long_ewma * ( 1 - ( self.smoothing / (1 + self.l) ) )
        self.count += 1

    def toString(self):
        return "{:.3f}    {:.3f}".format( self.short_ewma, self.long_ewma )

    def short_average(self):
        return self.short_ewma if self.count > self.l else 0

    def long_average(self):
        return self.long_ewma if self.count > self.l else 0

def srttTrend(flowId, flow):
    t = flow[TIME]
    srtt = flow[SRTT]
    rate_est = flow[OPT_MAX_BW]
    probe_bw_start = flow[PROBE_BW_START_TIME]

    t0 = t[probe_bw_start]

    srttTrend = EWMATrend() #TimeSeriesTrend()
    rateTrend = EWMATrend() #TimeSeriesTrend()

    srtt_long = []
    srtt_short = []
    srtt_count = []
    rate_long = []
    rate_short = []
    rate_count = []
    rate_diff = []
    trend_t = []
    for i in range( probe_bw_start+1, len(t) ):
        delta_t = t[i] - t0
        if delta_t >= 5: #srtt_start:

            #print(delta_t)
            srttTrend.add(srtt[i])
            rateTrend.add(rate_est[i])

            trend_t.append(t[i])
            srtt_short_average = srttTrend.short_average()
            srtt_long_average = srttTrend.long_average()
   
            rate_short_average = rateTrend.short_average()
            rate_long_average = rateTrend.long_average()

            srtt_short.append(srtt_short_average)
            rate_short.append(rate_short_average/1000)
            srtt_long.append(srtt_long_average)
            rate_long.append(rate_long_average/1000)
            if rate_long_average > 0:
                #rate_diff.append(100 * ((rate_short_average - rate_long_average) / rate_long_average) )
                rate_diff.append( 1 if rate_short_average > 1.02 * rate_long_average else 0 )
            else:
                rate_diff.append(0)

            #if srtt_short_average > srtt_long_average:
            #    srtt_count.append( srtt_count[-1] + 1 if len(srtt_count) > 0 else 1 )
            #else:
            #    srtt_count.append( 0 )
            if rate_diff[-1] >= 5:
                rate_count.append( 1 ) # rate_count[-1] + 1 if len(rate_count) > 0 else 1 )
            else:
                rate_count.append( 0 )
            #if rate_short_average > rate_long_average:
            #    rate_count.append( rate_count[-1] + 1 if len(rate_count) > 0 else 1 )
            #else:
            #    rate_count.append( 0 )

            #print("{} {} {}".format(t[i], srtt_short_average, srtt_long_average))
            t0 = t[i]

    plt.clf()
    fig, ax1 = plt.subplots()
    
    #ax1.plot(trend_t, srtt_short, linewidth=0.5, label='srtt short', color='red')
    #ax1.plot(trend_t, srtt_long, '--', linewidth=0.5, label='srtt long', color='red')
    #ax1.plot(trend_t, srtt_count, linewidth=0.5, label='count', color='red')
    ax1.plot(trend_t, rate_diff, linewidth=0.5, label='delta', color='red')
    ax1.legend()
    ax2 = ax1.twinx()
    ax2.plot(trend_t, rate_short, linewidth=0.5, label='rate short', color='blue')
    ax2.plot(trend_t, rate_long, '--', linewidth=0.5, label='rate long', color='blue')
    ax2.plot(trend_t, rate_count, linewidth=0.5, label='count', color='blue')
    plt.legend()
    fig.tight_layout()
    #plt.savefig("{}_trend.jpg".format(flowId))

if args.summary:
    for flowId in sorted(flows.keys()):
        flow = flows[flowId]
        ue = "-"
        if flowId in flow2ue:
            ue = flow2ue[flowId]
        #t = flow[TIME]
        #dur = t[-1] - t[0]
        #size = flow[BYTES][-1] - flow[BYTES][0]
        #tput = 0
        #if dur > 0:
        #    tput = (size * 8 / 1000)/ dur  # converting to mbps
        #print("{} {} {:6} start {:6} duration {:10} bytes {:10} tput {:0.3f}".format(ue, flowId, len(t), t[0], t[-1] - t[0], flow[BYTES][-1] - flow[BYTES][0], tput))
        print("summary for {} {}".format(flowId, len(flow[TIME])))
        if len(flow[TIME]) > 0:
            print( summaryString(flowId, flow, ue) )

        #srttDelta(flowId, flow)

def setGraphAttributes(title, xlabel, ylabel):
    plt.title(title)
    plt.grid(color='k', linestyle=':', linewidth=0.5)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def filter( t, r, tmin, tmax):
    filteredValues = [ (tval, rval) for tval,rval in zip(t, r) if tval < tmax and tval >= tmin ]
    return zip(*(filteredValues)) if len(filteredValues) else ([], [])

def plotScatter(plot, flows, x, y, title, xlabel, ylabel):
    for flowId in flows.keys():
        flow = flows[flowId]
        t = flow[x]
        r = flow[y]
        print("{} : {} : {} : t[{}] r[{}]".format(flowId, flowId.split('-')[0], ylabel, len(t), len(r)))
        plt.scatter(t, r, s=0.5, label=flowId.split('-')[0])
    setGraphAttributes(title, xlabel, ylabel)

def plotGraph(plot, flows, x, y, title, xlabel, ylabel):
    for flowId in flows.keys():
        flow = flows[flowId]
        t = flow[x]
        r = flow[y]
        plt.plot(t, r, linewidth=0.8, label=flowId.split('-')[0])
    setGraphAttributes(title, xlabel, ylabel)

tmpDir = tempfile.mkdtemp()
imgFormat = "jpg"

def plotAllFlows(plot, flows, title, xkey, ykey, xlabel, ylabel, ylim, y2key, y2label, y2lim):
    numSubPlots = len(flows.keys())
    nx = 1
    ny = 1

    if numSubPlots > 1:
        nx = math.ceil(numSubPlots/2)
        ny = 2

    #print("{} {}".format(nx,ny))
    fig, axs = plot.subplots(nx, ny, sharex=True)
    fig.suptitle(title)
    fig.set_size_inches(24,24)
    sp = 0

    for xplt in range(0,nx):
        for yplt in range(0,ny):
            sp = xplt * ny + yplt
            #print("{} {} {}".format(xplt, yplt, sp))
            if sp >= numSubPlots:
                break
            flowId = list(flows.keys())[sp]
            flow = flows[flowId]
            t = flow[xkey]
            y = flow[ykey]

            if nx > 1:
                if ny > 1:
                    ax1 = axs[xplt][yplt]
                else:
                    ax1 = axs
            else:
                if ny > 1:
                    ax1 = axs[yplt]
                else:
                    ax1 = axs
            
            ax2 = ax1.twinx()

            ax1.plot(t, y, linewidth=1.5)
            ax1.set_title(flowId)
            ax1.set_ylabel( ylabel )
            if ylim is not None:
                ax1.set_ylim( ylim )
            ax1.grid(color='k', linestyle=':', linewidth=0.5)
            if y2key is not None:
                y2 = flow [ y2key ]
                ax2.plot(t, y2, linewidth=1.5, linestyle = '--', color='red')
                ax2.set_ylabel( y2label )
                if y2lim is not None:
                    ax2.set_ylim( y2lim )

if args.perms:
    print("{}-per-ms.csv".format(args.outfile))
    with open("{}-per-ms.csv".format(args.outfile), "w") as csv:
        csv.write("{},{},{},{},{},{}\n".format("ms", "count", "active", "rtt", "inflight","rate"))

        t = []
        rtt = []
        inflight = []
        rate = []
        pacing_rate = []
        active = []
        for per_ms_data in per_ms:
            csv.write("{},{},{},{},{},{}\n".format(per_ms_data.t, per_ms_data.count, per_ms_data.active, per_ms_data.rtt, per_ms_data.inflight, per_ms_data.rate))
            t.append(per_ms_data.t)
            rtt.append(per_ms_data.rtt)
            inflight.append(per_ms_data.inflight)
            rate.append(per_ms_data.rate)
            pacing_rate.append(per_ms_data.pacing_rate)
            active.append(per_ms_data.active)

        ps=10
        fig, axs = plt.subplots(3,1, sharex=True)
        fig.suptitle("{}-per-ms".format(args.outfile))
        fig.set_size_inches(24,24)
        ax1 = axs[0]
        ax1.set_title("rate")
        ax1.scatter(t, rate, s=ps, label="rate")
        ax1.set_ylim([0, 800])
        ax1.set_ylabel("rate")
        ax1.grid(color='k', linestyle=':', linewidth=0.5)
        y2 = ax1.twinx()
        y2.scatter(t, active, s=ps, label="active", color="red", linestyle='--')
        y2.set_ylim([0, 20])
        y2.set_ylabel("active")


        ax2 = axs[1]
        ax2.set_title("rtt | inflight")
        ax2.scatter(t, rtt, s=ps, label="rtt")
        ax2.set_ylim([0, 350])
        ax2.set_ylabel("rtt")
        ax2.grid(color='k', linestyle=':', linewidth=0.5)
        y2 = ax2.twinx()
        y2.scatter(t, inflight, s=ps, label="inflight", color="red", linestyle='--')
        y2.set_ylim([0, 25000])
        y2.set_ylabel("inflight")

        ax3 = axs[2]
        ax3.set_title("pacing rate | estimated rate")
        ax3.scatter(t, pacing_rate, s=ps, label="rate")
        ax3.set_ylim([0, 1600])
        ax3.set_ylabel("pacing rate")
        ax3.grid(color='k', linestyle=':', linewidth=0.5)
        y2 = ax3.twinx()
        y2.scatter(t, rate, s=ps, label="rate", color="red", linestyle='--')
        y2.set_ylim([0, 1600])
        y2.set_ylabel("rate")

        pltFile = "{}-per-ms.{}".format(args.outfile, imgFormat)
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        plt.close()


if args.csv:
    for flowId in flows.keys():
        print("writing {}.csv".format(flowId))
        with open("{}.csv".format(flowId), "w") as csv:
            flow = flows[flowId]

            vals = []
            for graph in enabledGraphs:
                val = graphs[graph]["y"]
                if val not in vals:
                    vals.append(val)

            csv.write("{}".format(TIME))
            for val in vals:
                if val == TIME:
                    continue
                else:
                    csv.write(",{}".format(val))
            csv.write("\n")

            for i in range(0,len(flow[TIME])):
                t = flow[TIME][i]
                csv.write("{}".format(t))
                for val in vals:
                    if val == TIME:
                        continue
                    else:
                        v = flow[val]
                        csv.write(",{}".format(flow[val][i]))
    
                csv.write("\n")
    
if not args.outfile:
   sys.exit(0) 

print("writing images to {}.zip using {}".format(args.outfile, tmpDir))
with zipfile.ZipFile("{}.zip".format(args.outfile), mode='w') as zf:
    with open("summary.txt", "w") as summaryFile:

        plotAllFlows(plot=plt, flows=flows, title="loss-cwnd", xkey=TIME, ykey=RS_LOST_PERCENT, xlabel="Time (ms)", ylabel="loss rate %.", ylim=[0,100], y2key=CWND, y2label="cwnd", y2lim = [0, args.cwnd_limit])
        pltFile = os.path.join(tmpDir, "{}-flows-loss-cwnd.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="loss-rtt_count", xkey=TIME, ykey=LOSS_RATE_EXCEEDED_CNT, xlabel="Time (ms)", ylabel="loss rtt count", ylim=[0,10], y2key=INFLIGHT, y2label="inflight", y2lim = [0, 3000])
        pltFile = os.path.join(tmpDir, "{}-flows-loss-rtt-count-inflight.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="loss-rtt_count", xkey=TIME, ykey=LOSS_RATE_EXCEEDED_CNT, xlabel="Time (ms)", ylabel="loss rtt count", ylim=[0,10], y2key=RATE, y2label="pacing", y2lim = [0, 200])
        pltFile = os.path.join(tmpDir, "{}-flows-loss-rtt-count-pacing.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="loss-rate-inflight", xkey=TIME, y2key=INFLIGHT, xlabel="Time (ms)", y2label="inflight.", y2lim=[0,3000], ykey=RS_LOST_PERCENT, ylabel="loss rate percent", ylim = [0, 40])
        pltFile = os.path.join(tmpDir, "{}-flows-loss-rate-inflight.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="loss-rate-rtt", xkey=TIME, ykey=RS_LOST_PERCENT, xlabel="Time (ms)", ylabel="loss rate %.", ylim=[0,40], y2key=SRTT, y2label="rtt", y2lim = [0, 300])
        pltFile = os.path.join(tmpDir, "{}-flows-loss-rate-rtt.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="loss - cwnd-gain", xkey=TIME, ykey=RS_LOST_PERCENT, xlabel="Time (ms)", ylabel="loss rate %.", ylim=[0,10], y2key=OPT_CWND_GAIN, y2label="cwnd gain", y2lim = (0, 1200))
        pltFile = os.path.join(tmpDir, "{}-flows-loss-cwnd-gain.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="cwnd-inflight", xkey=TIME, ykey=CWND, xlabel="Time (ms)", ylabel="cwnd", ylim=(0,args.cwnd_limit), y2key=INFLIGHT, y2label="inflight", y2lim=(0,args.cwnd_limit))
        pltFile = os.path.join(tmpDir, "{}-flows-cwnd-inflight.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="mode-inflight", xkey=TIME, ykey=OPT_MODE, xlabel="Time (ms)", ylabel="mode", ylim=(0,3), y2key=INFLIGHT, y2label="inflight", y2lim=(0,args.cwnd_limit))
        pltFile = os.path.join(tmpDir, "{}-flows-mode-inflight.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="pacing-gain", xkey=TIME, ykey=OPT_PACING_GAIN, xlabel="Time (ms)", ylabel="pacing-gain", ylim=(0,4), y2key=OPT_CWND_GAIN, y2label="cwnd-gain", y2lim=(0,1024))
        pltFile = os.path.join(tmpDir, "{}-flows-gains.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="pacing - bw", xkey=TIME, ykey=RATE, xlabel="Time (ms)", ylabel="pacing", ylim=(0,200), y2key=CWND, y2label="cwnd", y2lim=(0,args.cwnd_limit))
        pltFile = os.path.join(tmpDir, "{}-flows-pacing-cwnd.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="pacing - bw", xkey=TIME, ykey=RATE, xlabel="Time (ms)", ylabel="pacing", ylim=(0,200), y2key=RS_RATE_EST, y2label="bw", y2lim=(0,200))
        pltFile = os.path.join(tmpDir, "{}-flows-pacing-bw.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="delivered-inflight", xkey=TIME, ykey=DELIVERED, xlabel="Time (ms)", ylabel="inflight", ylim=None, y2key=INFLIGHT, y2label="inflight", y2lim=(0,args.cwnd_limit))
        pltFile = os.path.join(tmpDir, "{}-flows-delivered-inflight.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="rtt - inflight", xkey=TIME, ykey=SRTT, xlabel="Time (ms)", ylabel="rtt", ylim=(0,500), y2key=INFLIGHT, y2label="inflight", y2lim=(0,args.cwnd_limit))
        pltFile = os.path.join(tmpDir, "{}-flows-rtt-inflight.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="rtt", xkey=TIME, ykey=SRTT, xlabel="Time (ms)", ylabel="rtt", ylim=(0,500), y2key=RS_RATE_EST, y2label="bw", y2lim=(0,200))
        pltFile = os.path.join(tmpDir, "{}-flows-rtt-bw.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()
    
        plotAllFlows(plot=plt, flows=flows, title="bw_max", xkey=TIME, ykey=BW_MAX0, xlabel="Time (ms)", ylabel="bw max 0", ylim=None, y2key=BW_MAX2, y2label="bw max 2", y2lim=None)
        pltFile = os.path.join(tmpDir, "{}-flows-bw-max.{}".format(args.outfile, imgFormat))
        print("Adding {}".format(pltFile))
        plt.savefig(pltFile)
        zf.write(pltFile, os.path.basename(pltFile))
        plt.close()

        if args.perflow:
            for flowId in flows.keys():
                flow = flows[flowId]
                t = flow[TIME]

                if len(t) == 0:
                    print("skipping {}".format(flowId))
                    continue
                ue = "-"
                if flowId in flow2ue:
                    ue = flow2ue[flowId]
            
                #summaryFile.write("{} {} {:6} start {:6} duration {:10} bytes {:10}\n".format(ue, flowId, len(t), t[0], t[-1] - t[0], flow[BYTES][-1] - flow[BYTES][0]))
                summaryFile.write(summaryString(flowId, flow, ue) + os.linesep)

                numSubPlots = len(enabledGraphs)

                if numSubPlots > 1:
                    fig, axs = plt.subplots(numSubPlots, sharex=True)
                    fig.suptitle(flowId)
                    fig.set_size_inches(8,12)
                    for i in range(numSubPlots):
                        graph = graphs[ enabledGraphs[i] ]
                        t = flow[TIME]
                        r = flow [ graph["y"] ]

                        axs[i].plot(t, r, linewidth=1)
                        axs[i].set_ylabel( graph["ylabel"] )
                        axs[i].grid(color='k', linestyle=':', linewidth=0.5)

                        if args.min_time:
                            axs[i].set_xlim( [args.min_time, None] )

                        if "ylim" in graph:
                            axs[i].set_ylim( graph["ylim"] )

                        if "y12" in graph:
                            y12 = flow [ graph["y12"] ]
                            axs[i].plot(t, y12, linewidth=0.8, linestyle = '--', color='red')

                        if "y2" in graph:
                            y2 = flow [ graph["y2"] ]
                            ax2 = axs[i].twinx()
                            ax2.plot(t, y2, linewidth=0.8, linestyle = '--', color='red')
                            ax2.set_ylabel( graph["y2label"] )
                            if "y2lim" in graph:
                                ax2.set_ylim( graph["y2lim"] )

                else:
                    graph = graphs[ enabledGraphs[0] ]
                    r = flow [ graph["y"] ]
                    plt.plot(t, r, linewidth=1)
                    plt.ylabel( graph["ylabel"] )
                    plt.grid(color='k', linestyle=':', linewidth=0.5)
                    if args.min_time:
                        axs[i].set_xlim( [args.min_time, None] )

                    if "ylim" in graph:
                        axs[i].set_ylim( graph["ylim"] )

                    if "y12" in graph:
                        y12 = flow [ graph["y12"] ]
                        plt.plot(t, y12, linewidth=0.8, linestyle = '--', color='red')

                    if "y2" in graph:
                        y2 = flow [ graph["y2"] ]
                        ax2 = plt.twinx()
                        ax2.plot(t, y2, linewidth=0.8, linestyle = '--', color='red')
                        ax2.set_ylabel( graph["y2label"] )
                        if "y2lim" in graph:
                            ax2.set_ylim( graph["y2lim"] )

                pltFile = os.path.join(tmpDir, "{}.{}".format(flowId, imgFormat))
                print("Adding {}".format(pltFile))
                plt.savefig(pltFile)
                zf.write(pltFile, os.path.basename(pltFile))
                plt.close()

                srttTrend(flowId, flow)
                pltFile = os.path.join(tmpDir, "{}-trend.{}".format(flowId, imgFormat))
                plt.savefig(pltFile)
                zf.write(pltFile, os.path.basename(pltFile))
                plt.close()

    zf.write("summary.txt")


