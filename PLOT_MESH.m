close all
clear
clc

% Coordenadas
coord = dlmread('coord.txt');


% Topología
top =dlmread('top.txt');
top = top(:, 2:end)

% Plot

plot(coord,marker="*",Color="red",LineStyle="none")
figure
opt=struct('LabelEle', 15, 'LabelNode', 14,'LineStyle','-','EdgeColor','b','LineWidth', 1)
PTRIMESH(coord,top,opt)
title('FIGURA 1: MALLA');