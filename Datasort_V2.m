function Datasort_V2(saveName)

%Author: Logan Manlove                                 
%Created: 10/28/2014
%Edited: 3/13/2015
%Purpose: Datasort was created to sort a specific set of data
% 
%Datasort takes no inputs at the command line but once the function is
%   running it asks the user to input three excel files, with data in first
%   worksheet of file, (score, PT_Map, PT_Info). The data is then written
%   to a excel file titled 'infoFinal.xls' which is created in the same 
%   folder as the PT_Info file
% 
% Datasort(saveName) takes a string with or without a file extension as an
%   input and saves the data to an excel file with the saveName.
%
% Data in the excel sheet can then be sorted by patient number to group the
% patient numbers together.


% Datasort starts by requesting the user select three excel files from a
% folder. Datasort is set up to initally attempt to open the pabel folder
% in ventura, if that fails it opens the matlab folder. Once the first
% folder is selected the function retains the folder path for the
% subsequent selections.

% try
%     [score, map] = uigetfile({'*.*'},'Select ''Score'' excel file', 'Z:\I\pabel\');
% catch
%     [score, map] = uigetfile({'*.*'},'Select ''Score'' excel file');
% end
% [PTmap, map] = uigetfile({'*.*'}, 'Select Pt map excel file', map);
% [Ptinfo] = uigetfile({'*.*'}, 'Select Pt Info excel file', map);

% The next block checks if saveName is a string and then if it has a file extension
% If saveName was not given or it is not a string 'infoFinal.xls' is stored
% for saveName. If it is a string but no file extension is found '.xls' is
% added to the string.

score = 'Z:\I\pabel\Laboratory\Personnel\grad students\Karuna\TMA Analysis\TMA slide 007.xlsx';
Ptinfo = 'Z:\I\pabel\Laboratory\Personnel\grad students\Karuna\TMA Analysis\Copy of TMAS 7 and 10 blinded 2014Aug11.xlsx';
PTmap = 'Z:\I\pabel\Laboratory\Personnel\grad students\Karuna\TMA Analysis\OVCA7 map file.xlsx';
map = 'Z:\I\pabel\Laboratory\Personnel\grad students\Karuna\TMA Analysis\';


try
    if iscellstr({saveName}) == 1
        if ismember('.', saveName) == 0
            saveName = strcat(saveName, '.xls');
        end
    elseif iscellstr({savName}) == 0
        saveName = 'infoFinal.xls';
    end
catch
    saveName = 'infoFinal.xls';
end

% files are read from excel into arrays
score = xlsread(score);
[PTinfoN, ~, PTinfoS] = xlsread(Ptinfo);
PTmap = xlsread(PTmap);

len = length(score);
[checkrow, checkcol] = size(PTmap);
infoFinal = cell(len + 1, 108);

% Titles for the collected data array are added.
infoFinal(1, 12:108) = PTinfoS(1, 2:98);
infoFinal(1, 1) = {'Pt Number'};
infoFinal(1, 2) = {'Tumor %'};
infoFinal(1, 3) = {'Tumor Intensity'};
infoFinal(1, 5) = {'Other %'};
infoFinal(1, 6) = {'Other Intensity'};
infoFinal(1, 8) = {'Row'};
infoFinal(1, 9) = {'Column'};
infoFinal(1, 10) = {'Grade'};
infoFinal(1, 11) = {'Stage'};

% Datasort steps through the score array and saves the row and columns that
% correspond to the map array. These values along with the % and Intensity
% scores are saved to the final data array
for i = 1:len
    % Find the row and column form the score file to use the map file to
    % find the PT number
    rowTemp = score(i, 1) + 1;
    colTemp = score(i, 2) + 1;
    
    % Save the row and column numbers to the final sheet
    infoFinal(i + 1, 8) = {rowTemp - 1};
    infoFinal(i + 1, 9) = {colTemp - 1};
    
    % Save the tumor scores and intensities
    tumorPer = score(i, 3);
    tumorInt = score(i, 4);
    otherPer = score(i, 7);
    otherInt = score(i, 8);
    
    % Save the scores and intensities to the final sheet
    infoFinal(i + 1, 2) = {tumorPer};
    infoFinal(i + 1, 3) = {tumorInt};
    infoFinal(i + 1, 5) = {otherPer};
    infoFinal(i + 1, 6) = {otherInt};  
    
    % Uses the tumor scores and intensities to classify the tumor.
    % If Intensity = 0 -> none
    % If Intensity = 1 -> Low
    % If Intensity = 2 and percent is zero or one -> Low
    % If Intensity = 2 and percent is two or three -> Moderate
    % If Intensity = 3 and percent is zero or one -> Moderate
    % If Intensity = 3 and percent is two or three -> Strong
    % These classifications are saved to the final sheet
    
    % First classification is done on the tumor grades
    if tumorInt == 0;
        if tumorPer == 0;                           % 0:0 (None)
            infoFinal(i+1, 4) = {'None'};       
        elseif tumorPer > 0 && tumorPer < 4;        % 0:1-3 (Weak)
            infoFinal(i+1, 4) = {'Weak'};
        elseif tumorPer > 3;                        % 0:4 (Not Accessed)
            infoFinal(i+1, 4) = {'Not Accessed'};
        end
    elseif tumorInt == 1;
        if tumorPer > 0 && tumorPer < 3;            % 1:1-2 (Weak)
            infoFinal(i+1, 4) = {'Weak'};
        elseif tumorPer == 3;                       % 1:3 (Moderate)
            infoFinal(i+1, 4) = {'Moderate'};
        elseif tumorPer > 3;                        % 1:4 (Not Accessed)
            infoFinal(i+1, 4) = {'Not Accessed'};
        end
    elseif tumorInt == 2 || tumorInt == 3;
        if tumorPer == 1;                           % 2-3:1 (Weak)
            infoFinal(i+1, 4) = {'Weak'};
        elseif tumorPer == 2;                       % 2-3:2 (Moderate)
            infoFinal(i+1, 4) = {'Moderate'};
        elseif tumorPer == 3;                       % 2-3:3 (Strong)
            infoFinal(i+1, 4) = {'Strong'};
        elseif tumorPer == 4;                       % 2-3:4 (Not Accessed)
            infoFinal(i+1, 4) = {'Not Accessed'};
        end
    elseif tumorInt == 4;
        infoFinal(i+1, 4) = {'Not Accessed'};       % 4:~ (Not Accessed)
    end

    % The second set of classifications are done on the 'other' grades
    
    if otherInt == 0;
        if otherPer == 0;                           % 0:0 (None)
            infoFinal(i+1, 7) = {'None'};       
        elseif otherPer > 0 && otherPer < 4;        % 0:1-3 (Weak)
            infoFinal(i+1, 7) = {'Weak'};
        elseif otherPer > 3;                        % 0:4 (Not Accessed)
            infoFinal(i+1, 7) = {'Not Accessed'};
        end
    elseif otherInt == 1;
        if otherPer > 0 && otherPer < 3;            % 1:1-2 (Weak)
            infoFinal(i+1, 7) = {'Weak'};
        elseif otherPer == 3;                       % 1:3 (Moderate)
            infoFinal(i+1, 7) = {'Moderate'};
        elseif otherPer > 3;                        % 1:4 (Not Accessed)
            infoFinal(i+1, 7) = {'Not Accessed'};
        end
    elseif otherInt == 2 || tumorInt == 3;
        if otherPer == 1;                           % 2-3:1 (Weak)
            infoFinal(i+1, 7) = {'Weak'};
        elseif otherPer == 2;                       % 2-3:2 (Moderate)
            infoFinal(i+1, 7) = {'Moderate'};
        elseif otherPer == 3;                       % 2-3:3 (Strong)
            infoFinal(i+1, 7) = {'Strong'};
        elseif otherPer == 4;                       % 2-3:4 (Not Accessed)
            infoFinal(i+1, 7) = {'Not Accessed'};
        end
    elseif otherInt == 4;
        infoFinal(i+1, 7) = {'Not Accessed'};       % 4:~ (Not Accessed)
    end
    
       
    
    % If the saved row or column is larger than the size of the map array
    % no other data is collected
    if rowTemp <= checkrow && colTemp <= checkcol
        PTTemp = PTmap(rowTemp, colTemp);
        % The PT numbers that have been found are stored to a temporary
        % matrix to check against the new number.
        check = cell2mat(infoFinal(2:end,1));
        if ismember(PTTemp, check) == 0
            % If the number does not yet stored the PT number is checked
            % against the PT numbers in the PTinfo file and the location is
            % used to save the information to the final array.
            [logTemp, locTemp] = ismember(PTTemp, PTinfoN(:,1));
            if logTemp == 1;
                % Saves the grade and Stage to the final sheet
                infoFinal(i + 1, 10) = PTinfoS(locTemp + 1, 92);
                infoFinal(i + 1, 11) = PTinfoS(locTemp + 1, 95);
                
                % Saves all other patient information to the end of the
                % sheet.
                infoFinal(i + 1, 12:108) = PTinfoS(locTemp + 1, 2:98);
            end
        end

        infoFinal(i + 1,1) = {PTTemp};
    end
    
end

% saveName is added to the path found while selecting files and the final
% data array is written to an excel file and saved in the location
finalpath = strcat(map, saveName);
xlswrite(finalpath, infoFinal);

