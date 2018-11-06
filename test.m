clear ; close all; clc
% matlab code to convert excel output from MetaFluor to images.png
% 2016/05/01 Gehoon Chung

% Workflow:
% Read excel files
% get rid of NaNs
% find baseline and max value for F340/F380 ratio
% delete lines without positive response

debug = false;

if debug 
    files = {'20160420-4', '20160420-5', '20160420-6' }; 
    files = {'20160419-1', '20160419-2', '20160419-3', '20160419-5', '20160419-6', '20160420-1', '20160420-2', '20160420-3', '20160420-4', '20160420-5', '20160420-6' };
else
    files = {'20160419-1', '20160419-2', '20160419-3', '20160419-5', '20160419-6', '20160420-1', '20160420-2', '20160420-3', '20160420-4', '20160420-5', '20160420-6' };
end

folder = '/Users/gehoon/Project/Odontoblast_P2X/raw/CaImaging2016/';

% Initialization
rowName =[]; base=[]; peak=[]; ATP=[]; b2p=[]; b2ATP=[];

for fileName = files
    fn = strcat(folder,fileName,'.xlsx');
    disp (strcat('Reading :', fn));
    [~, sheets] = xlsfinfo(char(fn));
    
    for sh = sheets(1)
        disp (strcat('Processing :', sh));
        exp = Experiment(fn, sh);
        %exp.rowTitle;
        h = exp.plot();
        if debug
            print(h, strcat('/Users/gehoon/Desktop/',char(fileName)),'-djpeg');
        else
            print(h, strcat('/Users/gehoon/Project/Odontoblast_P2X/analysis/img/',char(fileName)),'-djpeg');
        end
        
        exp = exp.normalize();
        h = exp.plot();
        if debug
            print(h, strcat('/Users/gehoon/Desktop/',char(fileName),'_sel'),'-djpeg');
        else
            print(h, strcat('/Users/gehoon/Project/Odontoblast_P2X/analysis/img/','Sel_',char(fileName)),'-djpeg');
        end
    end
    
end