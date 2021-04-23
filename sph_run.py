import pysplishsplash as sph
from pysplishsplash.Extras import Scenes
import os
import sys
import json
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    assert(len(sys.argv) == 5), "sim_run.py should have 4 arguments."
    upload_config_file_path = sys.argv[1]
    upload_file_dir = sys.argv[2]
    upload_date_dir = sys.argv[3]
    sim_data_dir = sys.argv[4]

    # 为上传文件拼接上传目录
    f = open(upload_config_file_path, 'r')
    fileObj = json.loads(f.read())
    f.close()
    for obj in fileObj['RigidBodies']:
        obj['geometryFile'] = upload_file_dir+'/'+obj['geometryFile']
    fileObj_str = json.dumps(fileObj)
    f = open(upload_config_file_path, 'w')
    f.write(fileObj_str)
    f.close()

    # Set up the simulator
    base = sph.Exec.SimulatorBase()
    base.init(useGui=False,  sceneFile=upload_config_file_path,outputDir=sim_data_dir)
    #测试用
    #base.init(useGui=False,  sceneFile=upload_config_file_path)

    # Create an imgui simulator
    #gui = sph.GUI.Simulator_GUI_imgui(base)
    # base.setGui(gui)

    base.initSimulation()
    base.runSimulation()

    sim = sph.Simulation.getCurrent()
    numFluidParticles = 0
    for i in range(sim.numberOfFluidModels()):
    	numFluidParticles += sim.getFluidModel(i).numActiveParticles()
    numFrames = base.getFrameCounter()

    # 写sim_config_file
    root = ET.Element('Scene')
    root.set('name', '场景')

    simulationRun = ET.SubElement(root, 'SimulationRun')
    simulationRun.set('name', '模拟运行结果')

    frameSum = ET.SubElement(simulationRun, 'FrameSum')
    frameSum.set('name', '帧总数')
    frameSum.text = str(numFrames)

    animation = ET.SubElement(simulationRun, 'Animation')
    animation.set('name', '是否支持动画')
    animation.text = 'true'

    fluidParticleSum = ET.SubElement(simulationRun, 'Item')
    fluidParticleSum.set('name', '流体粒子总数')
    fluidParticleSum.text = str(numFluidParticles)

    tree = ET.ElementTree(root)
    sim_config_file_path = upload_date_dir+'/'+'sim_config_file.xml'
    tree.write(sim_config_file_path, encoding="utf-8", xml_declaration=True)

    base.cleanup()

    # 将路径输出到标准输出
    sys.stdout.write(sim_config_file_path)
