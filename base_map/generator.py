from pykml import parser
import matplotlib.pyplot as plt

file = './piste.kml'
root = parser.parse(file).getroot()
piste = root.Document.Folder

ima =  plt.imread("base.png")
height,width = len(ima),len(ima[0])
ratio = float(height/width)
dpi = 3000

style_dict={}
for pippo in root.iter('{http://www.opengis.net/kml/2.2}Style'):
    style_id = pippo.attrib['id']
    try:
        color = pippo.LineStyle.color
        width = pippo.LineStyle.width
    except AttributeError:
        color = '#000000' #black
        widht = 2.5

    style = {'style' : {'color':color, 'width':width}}
    style_dict[style_id] = style


for pippo in root.iter('{http://www.opengis.net/kml/2.2}StyleMap'):
    map_id = pippo.attrib['id']
    style_id = str(pippo.Pair.styleUrl)    

    if style_id[0] == '#':
        style_id = style_id[1:]

    color = style_dict[style_id]['style']['color']
    width = style_dict[style_id]['style']['width']

    style = {'style' : {'color':color, 'width':width}}
    style_dict[map_id] = style

#plt.figure(figsize=(height/dpi,width/dpi), dpi=dpi)

def plot_track(track):
    coords = str(track.LineString.coordinates)
    removal_list = [' ', '\t', '\n', ',0 ', '0 ']
    for s in removal_list:
        coords = coords.replace(s, '')

    coords_list = coords.split(",")
        
    x,y = [],[]
    for j in range(0,len(coords_list)-1,2):
        try:
            x.append(float(coords_list[j]))
            y.append(float(coords_list[j+1]))
        except ValueError:
            pass

    style_id = str(track.styleUrl)
    if style_id[0] == '#':
        style_id = style_id[1:]
    c = style_dict[style_id]['style']['color']
    w = style_dict[style_id]['style']['width']
    if c[0] != '#':
        c = '#'+c

    plt.plot(x, y, c=c, lw=w/dpi*100)


for tipo_pista in piste.Folder:
    for pista in tipo_pista.Placemark:
        plot_track(pista)
    #for sotto_tipo in tipo
    try:    
        for sotto_tipo_pista in tipo_pista.Folder:
            for pista in sotto_tipo_pista.Placemark:
                try:
                    plot_track(pista)
                except AttributeError:
                    pass
    except AttributeError:
        pass
        

implot = plt.imshow(ima, extent=[12.16125,12.60218, 45.2232,45.58447], aspect=ratio)
plt.tight_layout(pad=0)
plt.savefig('./prova.png', dpi=dpi)
    

