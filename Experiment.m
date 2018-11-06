classdef Experiment
    properties (Access = public)
        rowTitle; rowDrugN;
        %colR1Avg1; colR1Sum1; colR1Avg2; colR1Sum2; colR1R1;
        colAvg1; colSum1; colAvg2; colSum2; colR1;
        numeric; txt; raw
        drugs; drugTime;
        figH;
    end
    properties (Access = private)
        rn; cn;
        rr; cr;
        fn; sh;
    end
    
    methods
        function obj = Experiment(fn, sh)
            obj.fn = fn;
            obj.sh = sh;
            [obj.numeric, obj.txt, obj.raw] = xlsread(char(fn), char(sh));
            [obj.rn, obj.cn] = size(obj.numeric);
            [obj.rr, obj.cr] = size(obj.raw);
            
            obj = obj.setTitles();
            % Ratio가 소수점 2자리에서 반올림 된 경우 Ratio값 다시 계산하기
            if (obj.numeric(2, obj.colR1(1)) * 100 - floor(obj.numeric(2, obj.colR1(1)) * 100)) == 0
                obj = obj.recalcR();
            end
                    
            obj.drugs = obj.txt(~cellfun(@isempty, obj.txt(:,2)),2);
            obj.drugTime = obj.numeric(~cellfun(@isempty, obj.txt(:,2)),1);
            [~, obj.rowDrugN] = ismember(obj.drugTime, obj.numeric(:,1));
        end
        
        function figH = plot(obj)
            numDrug = length(obj.drugs); %7;
            figH = figure();
            %disp(obj.figH);
            if ~isempty(obj.colR1)
                plot(obj.numeric(:, 1), obj.numeric(:, obj.colR1));
                lastLabel = '';
                for idx =  1:numDrug
                    labelRow = obj.rowDrugN(idx);
                    %disp(labelRow);
                    labelX = obj.numeric(obj.rowDrugN(idx),1);
                    %disp(labelX);
                    labelY = min(min(obj.numeric(:,obj.colR1)));
                    labelTxt = obj.txt(obj.rowDrugN(idx)+1,2);
                    if ~strcmpi(labelTxt,lastLabel)
                        text(labelX, labelY, labelTxt);
                        %disp(labelTxt);
                        lastLabel = labelTxt;
                    end
                end
            end
        end
        
        function obj = normalize(obj)
            baseThr = 0.1;
            peakThr = 0.1;
            idxLast = -31;
            drugRow = [];
            for idx = obj.rowDrugN(1:end)'
                if idxLast < idx-30
                    idxLast = idx;
                else
                    drugRow = [drugRow idxLast];
                end
            end
            %disp(drugRow);
            
            %meanSpan = min(75,drugRow(1));            
            if ~isempty(drugRow) && (length(drugRow) > 2)
                base1 = mean(obj.numeric(max(drugRow(1)-60,2):drugRow(1)-1,obj.colR1));
                base3 = mean(obj.numeric(drugRow(3)-60:drugRow(3)-1,obj.colR1));
                k = find(abs(base3 - base1) < baseThr);
                obj.colR1 = obj.colR1(k);

                base1 = mean(obj.numeric(max(drugRow(1)-60,2):drugRow(1)-1,obj.colR1));
                peak1 = max(obj.numeric(drugRow(1)+1:drugRow(1)+60,obj.colR1));
                k = find((peak1 - base1) > peakThr);
                obj.colR1 = obj.colR1(k);

                base3 = mean(obj.numeric(drugRow(3)-60:drugRow(3)-1,obj.colR1));
                peak3 = max(obj.numeric(drugRow(3)+1:drugRow(3)+60,obj.colR1));
                k = find((peak3 - base3) > peakThr);
                obj.colR1 = obj.colR1(k);
                
                %base2 = mean(obj.numeric(drugRow(2)-60:drugRow(2)-1,obj.colR1));
                %peak2 = max(obj.numeric(drugRow(2)+1:drugRow(2)+60,obj.colR1));
            end

        end    
    end

    
    methods(Access = private)
        
        function obj = setTitles(obj)
            titleRowN = find(strcmpi('Time (sec)', obj.raw(:,1)),1,'last');
            if isempty(titleRowN)
                disp('### Title row does not exist. ###');
            else
                obj.rowTitle = obj.raw(titleRowN, :);
                obj.raw = obj.raw(titleRowN:end, :);
                obj.txt = obj.txt(titleRowN:end, :);
            end
                        
            colR1Avg1 = find(strcmpi('R1 W1 Avg', obj.rowTitle),1,'last');
            colR1Sum1 = find(strcmpi('R1 W1 Sum', obj.rowTitle),1,'last');
            colR1Avg2 = find(strcmpi('R1 W2 Avg', obj.rowTitle),1,'last');
            colR1Sum2 = find(strcmpi('R1 W2 Sum', obj.rowTitle),1,'last');
            colR1R1 = find(strcmpi('R1 R1', obj.rowTitle),1,'last');

            obj.colAvg1 = colR1Avg1:colR1R1-1:obj.cn;
            obj.colSum1 = colR1Sum1:colR1R1-1:obj.cn;
            obj.colAvg2 = colR1Avg2:colR1R1-1:obj.cn;
            obj.colSum2 = colR1Sum2:colR1R1-1:obj.cn;
            obj.colR1 = colR1R1:colR1R1-1:obj.cn;

            % Find last "clock reset to zero"
            zeroClock = find(strcmpi('Clock reset to 0.0', obj.txt(:,2)),1,'last');
            if isempty(zeroClock) || zeroClock < titleRowN
                zeroClock = titleRowN;
            end
            obj.raw = obj.raw(zeroClock+1:end, :);
            obj.txt = obj.txt(zeroClock+1:end, :);
            obj.numeric = obj.numeric(zeroClock+1:end, :);
            
        end
        
        function obj = recalcR(obj)
            if ~isempty(obj.colSum2)
                obj.numeric(:,obj.colR1) = obj.numeric(:,obj.colSum1) ./ obj.numeric(:,obj.colSum2);
            elseif ~isempty(obj.colAvg2)
                obj.numeric(:,obj.colR1) = obj.numeric(:,obj.colAvg1) ./ obj.numeric(:,obj.colAvg2);
            else
                disp('Need intensity signal data.');
            end
        end
                
    end
end
