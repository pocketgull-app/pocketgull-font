function theme_pocketgull(varargin)
% THEME_POCKETGULL Apply PocketGull clinical typography to MATLAB figures
%
% Applies Louise Sloan 5:1 optotypic clarity, high-contrast grid lines,
% and ISMP character disambiguation fonts to active or specified MATLAB figures.
%
% Syntax:
%   theme_pocketgull()
%   theme_pocketgull('Mode', 'scotopic')
%   theme_pocketgull('Figure', figHandle)
%   theme_pocketgull('FontSize', 12)
%
% Inputs (Optional Parameter-Value Pairs):
%   'Mode'     - 'light' (default) or 'scotopic' (circadian 650nm red OLED-safe)
%   'Figure'   - Target figure handle (default: gcf)
%   'FontSize' - Base font size in points (default: 11)
%
% Example:
%   plot(rand(10,1));
%   title('Telemetry Assay Run 01');
%   xlabel('Time (ms)');
%   ylabel('Voltage (\muV)');
%   theme_pocketgull();

    p = inputParser;
    addParameter(p, 'Mode', 'light', @(x) any(validatestring(x, {'light', 'scotopic'})));
    addParameter(p, 'Figure', [], @(x) isempty(x) || isgraphics(x, 'figure'));
    addParameter(p, 'FontSize', 11, @isnumeric);
    parse(p, varargin{:});

    fig = p.Results.Figure;
    if isempty(fig)
        fig = gcf;
    end
    
    mode = p.Results.Mode;
    baseFontSize = p.Results.FontSize;
    fontName = 'PocketGull';

    % Color definitions
    if strcmpi(mode, 'scotopic')
        bgColor    = [0.035, 0.035, 0.043]; % #09090b
        textColor  = [0.957, 0.247, 0.369]; % #f43f5e (650nm Red)
        gridColor  = [0.153, 0.153, 0.165]; % #27272a
        axisColor  = [0.882, 0.114, 0.282]; % #e11d48
    else
        bgColor    = [1.000, 1.000, 1.000]; % #ffffff
        textColor  = [0.094, 0.094, 0.106]; % #18181b
        gridColor  = [0.957, 0.957, 0.961]; % #f4f4f5
        axisColor  = [0.443, 0.443, 0.478]; % #71717a
    end

    % Configure Figure
    set(fig, 'Color', bgColor);

    % Configure all Axes children
    axesList = findall(fig, 'Type', 'axes');
    for i = 1:length(axesList)
        ax = axesList(i);
        set(ax, ...
            'FontName', fontName, ...
            'FontSize', baseFontSize, ...
            'XColor', axisColor, ...
            'YColor', axisColor, ...
            'ZColor', axisColor, ...
            'Color', bgColor, ...
            'GridColor', gridColor, ...
            'GridAlpha', 0.8, ...
            'LineWidth', 0.8, ...
            'Box', 'off', ...
            'TickDir', 'out');
        grid(ax, 'on');

        % Configure Titles and Labels
        if isprop(ax, 'Title') && ~isempty(ax.Title)
            set(ax.Title, ...
                'FontName', fontName, ...
                'FontSize', baseFontSize * 1.2, ...
                'FontWeight', 'bold', ...
                'Color', textColor);
        end
        if isprop(ax, 'Subtitle') && ~isempty(ax.Subtitle)
            set(ax.Subtitle, ...
                'FontName', fontName, ...
                'FontSize', baseFontSize * 0.95, ...
                'Color', textColor);
        end
        if isprop(ax, 'XLabel') && ~isempty(ax.XLabel)
            set(ax.XLabel, 'FontName', fontName, 'Color', textColor, 'FontWeight', 'bold');
        end
        if isprop(ax, 'YLabel') && ~isempty(ax.YLabel)
            set(ax.YLabel, 'FontName', fontName, 'Color', textColor, 'FontWeight', 'bold');
        end
    end
end
