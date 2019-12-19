#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Nov 12 15:20:04 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 480000
        self.rx_gain = rx_gain = 40
        self.fm_station = fm_station = 104e6

        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.rx_gain,
        	callback=self.set_rx_gain,
        	label="rx_gain",
        	converter=forms.float_converter(),
        )
        self.Add(self._rx_gain_text_box)
        _fm_station_sizer = wx.BoxSizer(wx.VERTICAL)
        self._fm_station_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_fm_station_sizer,
        	value=self.fm_station,
        	callback=self.set_fm_station,
        	label='fm_station',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._fm_station_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_fm_station_sizer,
        	value=self.fm_station,
        	callback=self.set_fm_station,
        	minimum=88e6,
        	maximum=108e6,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_fm_station_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="fft plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_source("external", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(fm_station, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0.set_bandwidth(200e3, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 100e3, firdes.WIN_BLACKMAN, 6.76))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((1, ))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_pll_0 = analog.wfm_rcv_pll(
        	demod_rate=samp_rate,
        	audio_decimation=10,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_pll_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.analog_wfm_rcv_pll_0, 1), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 1))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_pll_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 100e3, firdes.WIN_BLACKMAN, 6.76))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self._rx_gain_text_box.set_value(self.rx_gain)
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
        	

    def get_fm_station(self):
        return self.fm_station

    def set_fm_station(self, fm_station):
        self.fm_station = fm_station
        self._fm_station_slider.set_value(self.fm_station)
        self._fm_station_text_box.set_value(self.fm_station)
        self.uhd_usrp_source_0.set_center_freq(self.fm_station, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
