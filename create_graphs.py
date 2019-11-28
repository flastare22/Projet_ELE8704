from random import random
from pckt_info import pckt_info



def generate_random_pkts(nbr_pckt):
    random_pkts = []
    arrival_time = 0

    for i in range(nbr_pckt):

        new_pckt = pckt_info()
        new_pckt.size = random() * 500
        random_delay = random() * 30
        arrival_time += random_delay
        new_pckt.abs_arrival_time = arrival_time
        new_pckt.rel_arrival_time = random_delay
        new_pckt.is_resend = (round(random()*10) % 1 == 0)


def generate_size_histogram(youtube_wifi, youtube_filaire):





def main():

    youtube_wifi = generate_random_pkts(500)
    youtube_filaire = generate_random_pkts(500)

    generate_size_histogram(youtube_wifi, youtube_filaire)

