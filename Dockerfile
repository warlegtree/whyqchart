#NCP summary charts
#Version 1.0

# Base images
FROM python:3.6-alpine

VOLUME /home

#MAINTAINER
MAINTAINER ezngzen

#Config pip.conf
RUN mkdir /root/.pip/
ADD pip.conf /root/.pip/

#install python module
RUN pip install requests pyecharts echarts-countries-pypkg echarts-china-provinces-pypkg echarts-china-cities-pypkg echarts-china-counties-pypkg echarts-china-misc-pypkg echarts-united-kingdom-pypkg
ADD yq.py /home

