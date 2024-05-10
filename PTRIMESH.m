function  PTRIMESH( coord, top, opt)
%Imprimir una malla de elementos triangulares
%
%Entradas
%    p(i,:)   - coordenadas del nodo i 
%    t(i,:)   - numeros nodales del triangulo i
%  opciones de impresion:
%    opt=struct('LabelEle', 10, 'LabelNode', 8, ...
%               'LineStyle','-','EdgeColor','k','LineWidth', 1)
%  las posibles opciones son 
%    opt.LabelEle  : = 0, No colocar etiquetas en los elementos;
%                      si se coloca cualquier otro valor entero positivo
%                      define el tamaño del numero de nodo
%    opt.LabelNode : = 0, No colocar etiquetas en los nodos
%                      si se coloca cualquier otro valor entero positivo
%                      define el tamaño del numero de nodo
%    opt.LineStyle, opt.EdgeColor, opt.LineWidth: otras opciones
%                                                 predefinidas para imagenes

%opciones por defecto
LineStyle = '-';   EdgeColor = 'k';  LineWidth = 1;
%usar opciones especificas si se presentan
if nargin > 2
    if isfield(opt, 'LineStyle') && ~isempty(opt.LineStyle)
        LineStyle = opt.LineStyle;
    end
    if isfield(opt, 'EdgeColor') && ~isempty(opt.EdgeColor)
        EdgeColor = opt.EdgeColor;
    end
    if isfield(opt, 'LineWidth') && ~isempty(opt.LineWidth)
        LineWidth = opt.LineWidth;
    end
end

%imprimir la malla triangular
patch('Faces',top,'Vertices',coord,'FaceColor','w',...
    'LineStyle',LineStyle,'EdgeColor',EdgeColor, ...
    'LineWidth',LineWidth);

axis equal; axis on; grid off;
hold on;

%Opciones graficas
if nargin > 2
    if isfield(opt, 'LabelNode') && opt.LabelNode %nodos
        if opt.LabelNode <= 2 %tamaño de fuente del numero de nodo
            fontsize = 14;
        else
            fontsize = opt.LabelNode;
        end
        %mostrar los nodos
        plot(coord(:,1),coord(:,2),'ko','LineWidth',LineWidth); 
        np = length(coord); %Numero de nodos
 
        text(coord(:,1), coord(:,2), [blanks(np)' int2str((1:np)')], ...
            'FontSize',fontsize ); %etiqueta de los nodos
    end
    if isfield(opt, 'LabelEle') && opt.LabelEle %elementos
        if opt.LabelEle <= 2 %tamaño de fuente del numero de elemento
            fontsize = 14;
        else
            fontsize = opt.LabelEle;
        end
        % calculo d ecentroides centroides
        triCnt = (coord(top(:,1),:)+coord(top(:,2),:)+coord(top(:,3),:))/3; 

        nTri = length(top); %numero de elementos triangulares

        text(triCnt(:,1),triCnt(:,2), ...
            [ int2str((1:nTri)')],...
            'FontSize',fontsize, 'Color','r'); %etiqueta de elementos en el centroide
    end
end