"use client";
import {CodeIcon, MixIcon} from "@radix-ui/react-icons"
import "../../../styles/blockly1.css"
import React, {useEffect, useState} from "react";
import {BlocklyWorkspace} from "react-blockly";
import {pythonGenerator} from 'blockly/python';
import Blockly from "blockly";
import "./toolbox_style.css"
import "./custom_blocks"
import {ClockIcon} from "lucide-react"
import {redirect, useParams} from 'next/navigation'

import {Button} from "@/registry/new-york/ui/button"
import {HoverCard, HoverCardContent, HoverCardTrigger,} from "@/registry/new-york/ui/hover-card"
import {Label} from "@/registry/new-york/ui/label"
import {Tabs, TabsContent, TabsList, TabsTrigger,} from "@/registry/new-york/ui/tabs"
import {Input} from "@/registry/new-york/ui/input"
import {Textarea} from "@/registry/new-york/ui/textarea"
import {getDefaultToolbox} from "@/app/rules/[id]/default_toolbox";
import {siteConfig} from "@/config/site";
import {timeSince} from "@/libs/timeSince";

export default function RuleEditorPage() {

    const params = useParams()

    // @ts-ignore
    const id = params.id || null;
    if (id === null) {
        redirect("/rules")
    }

    const [saved, setSaved] = useState(true)

    const [rule, setRule] = useState();

    const [workspaceIsInit, setWorkspaceIsInit] = useState(false);

    const [codeblock, setCodeblock] = useState("");
    const [workspaceXML, setWorkspaceXML] = useState<string | null>();
    const [workspaceXMLbase64, setWorkspaceXMLbase64] = useState<string | null>(null);

    useEffect(() => {

        //load rule from backend
        fetch(`${siteConfig.backend}/rules/${id}`).then((response) => {
            return response.json();
        }).then(
            (data) => {
                setRule(data)
                setWorkspaceXML(atob(data.workspace_xml))
                console.log(workspaceXML)
            }
        ).catch((err) => {
                console.log(err)
            }
        )
    }, []);

    function correctPythonIndentation(pythonCode: string) {
        let lines = pythonCode.split('\n');
        let newLines = [];
        let indentLevel = 0;
        let currentLine = '';

        for (let line of lines) {
            let trimmedLine = line.trim();

            if (trimmedLine.startsWith('def ') || trimmedLine.startsWith('class ')) {
                if (currentLine) newLines.push(currentLine);
                currentLine = ' '.repeat(indentLevel * 4) + trimmedLine;
                indentLevel = 1;
                continue;
            }

            if (trimmedLine.length === 0) {
                if (currentLine) newLines.push(currentLine);
                currentLine = '';
                newLines.push('');
                continue;
            }

            currentLine += ' ' + trimmedLine;
            if (trimmedLine.endsWith(':')) {
                newLines.push(currentLine);
                currentLine = '';
                indentLevel++;
            }
        }
        if (currentLine) newLines.push(currentLine);

        let l2 = newLines.map(line => {
            if (line.startsWith(' ') && line[1] !== ' ') {
                return line.substring(1);
            }
            return line;
        })
        return l2.map(line => {
            if (line.startsWith('return')) {
                return line.replace('return', '    return');
            }
            return line;
        }).join('\n')
    }


    function workspaceDidChange(workspace: Blockly.Workspace) {
        const xml: Element = Blockly.Xml.workspaceToDom(workspace)
        const xmlText = new XMLSerializer().serializeToString(xml);
        setWorkspaceXML(xmlText);
        setWorkspaceXMLbase64(btoa(xmlText));
        console.log(workspaceXMLbase64);

        let code = pythonGenerator.workspaceToCode(workspace);

        code = correctPythonIndentation(code);
        code = code.replaceAll("RULE_ID", rule.rule_id);
        setCodeblock(code);


        setSaved(false)

    }


    function handleSave() {
        //send post request to save the rule
        fetch(`${siteConfig.backend}/rules/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                _id: "string",
                rule_id: `rule-${id}`,
                active: true,
                name: rule.name,
                description: rule.description,
                last_updated: new Date().toISOString(),
                last_applied: new Date().toISOString(),
                workspace_xml: workspaceXMLbase64,
                function_code: codeblock,
            })
        }).then((response) => {
            setSaved(true);
        }).catch((err) => {
            console.log(err)
        });

    }

    return (
        <>
            <div className="container hidden h-full flex-col md:flex">
                <div className="flex-1 space-y-4 p-2 pt-6">
                    <div className="flex items-center justify-between space-y-2">
                        <h2 className="text-3xl font-bold tracking-tight">Rule Editor</h2>
                        <div className="flex items-center space-x-2">
                            {!saved &&
                                <div className={"text-xs text-red-500 flex items-center"}><b>Cautious</b>. You
                                    have&nbsp;
                                    <u>unsaved</u>&nbsp;changes.
                                </div>
                            }
                            <Button onClick={handleSave}>Save</Button>
                        </div>
                    </div>
                    <Tabs defaultValue="blocks" className="flex-1">
                        <div className="h-full py-6">
                            <div className="grid h-full items-stretch gap-6 md:grid-cols-[1fr_200px]">
                                <div className="hidden flex-col space-y-4 sm:flex md:order-2">
                                    <div className="grid gap-2">
                                        <HoverCard openDelay={200}>
                                            <HoverCardTrigger asChild>
                      <span
                          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                        View
                      </span>
                                            </HoverCardTrigger>
                                            <HoverCardContent className="w-[320px] text-sm" side="left">
                                                Switch between the rule editor mode and code mode.
                                            </HoverCardContent>
                                        </HoverCard>
                                        <TabsList className="grid grid-cols-2">
                                            <TabsTrigger value="blocks">
                                                <span className="sr-only">Blocks</span>
                                                <MixIcon/>
                                            </TabsTrigger>
                                            <TabsTrigger value="code">
                                                <span className="sr-only">Code</span>
                                                <CodeIcon/>
                                            </TabsTrigger>
                                        </TabsList>
                                    </div>

                                    <div className="grid gap-2">
                                        <Label htmlFor="rule-id">Rule ID</Label>
                                        <Input id="rule-id" placeholder="rule-1" value={rule && rule.rule_id}/>
                                    </div>
                                    <div className="grid gap-2">
                                        <Label htmlFor="description">Description</Label>
                                        <Textarea className={"h-[120px]"}
                                                  id="description"
                                                  placeholder="Please include all information relevant to this rule."
                                                  value={rule && rule.description}
                                        />
                                    </div>
                                    {/*<div className="grid gap-2">*/}
                                    {/*    <Label htmlFor="tags">Version</Label>*/}
                                    {/*    <p className="text-sm font-light leading-none">*/}
                                    {/*        {{rule && rule.version}}*/}
                                    {/*    </p>*/}
                                    {/*</div>*/}
                                    <div className="grid gap-2">
                                        <Label htmlFor="tags">Last Updated</Label>
                                        <p className="text-sm font-light leading-none">
                                            <ClockIcon className={"inline-block mr-1 h-4 w-4"}/>
                                            {rule && timeSince(rule.last_updated)} ago
                                        </p>
                                    </div>
                                    {rule && rule.last_applied && (<div className="grid gap-2">
                                        <Label htmlFor="tags">Last Applied</Label>
                                        <p className="text-sm font-light leading-none">
                                            <ClockIcon className={"inline-block mr-1 h-4 w-4"}/>
                                            {rule && rule.last_applied !== null && timeSince(rule.last_applied)} ago
                                        </p>
                                    </div>)}
                                </div>
                                <div className="md:order-1">
                                    <TabsContent value="code" className="mt-0 border-0 p-0">
                                        <div className="flex h-full flex-col space-y-4">
                                            <Textarea disabled={true} value={codeblock} readOnly={true}
                                                      placeholder="Start editing rules and the code appears here."
                                                      className="min-h-[400px] flex-1 p-4 md:min-h-[700px] lg:min-h-[700px]"
                                            />
                                        </div>
                                    </TabsContent>
                                    <TabsContent value="blocks" className="mt-0 border-0 p-0">
                                        <div className="flex h-full flex-col space-y-4">
                                            <div className="flex flex-col space-y-4">
                                                {workspaceXML && <BlocklyWorkspace
                                                    toolboxConfiguration={getDefaultToolbox()}
                                                    initialXml={workspaceXML}
                                                    workspaceConfiguration={
                                                        {
                                                            zoom: {
                                                                controls: true,
                                                                wheel: true,
                                                                startScale: 0.75,
                                                                maxScale: 4,
                                                                minScale: 0.25,
                                                                scaleSpeed: 1.1
                                                            },
                                                            grid: {
                                                                spacing: 20,
                                                                length: 2,
                                                                colour: "#ccc",
                                                                snap: true
                                                            }
                                                        }
                                                    }
                                                    className="fill-height"
                                                    onWorkspaceChange={workspaceDidChange}
                                                />}
                                            </div>
                                        </div>
                                    </TabsContent>
                                    <TabsContent value="insert" className="mt-0 border-0 p-0">
                                        <div className="flex flex-col space-y-4">
                                            <div
                                                className="grid h-full grid-rows-2 gap-6 lg:grid-cols-2 lg:grid-rows-1">
                                                <Textarea
                                                    placeholder="We're writing to [inset]. Congrats from OpenAI!"
                                                    className="h-full min-h-[300px] lg:min-h-[700px] xl:min-h-[700px]"
                                                />
                                                <div className="rounded-md border bg-muted"></div>
                                            </div>
                                        </div>
                                    </TabsContent>
                                    <TabsContent value="edit" className="mt-0 border-0 p-0">
                                        <div className="flex flex-col space-y-4">
                                            <div className="grid h-full gap-6 lg:grid-cols-2">
                                                <div className="flex flex-col space-y-4">
                                                    <div className="flex flex-1 flex-col space-y-2">
                                                        <Label htmlFor="input">Input</Label>
                                                        <Textarea
                                                            id="input"
                                                            placeholder="We is going to the market."
                                                            className="flex-1 lg:min-h-[580px]"
                                                        />
                                                    </div>
                                                    <div className="flex flex-col space-y-2">
                                                        <Label htmlFor="instructions">Instructions</Label>
                                                        <Textarea
                                                            id="instructions"
                                                            placeholder="Fix the grammar."
                                                        />
                                                    </div>
                                                </div>
                                                <div
                                                    className="mt-[21px] min-h-[400px] rounded-md border bg-muted lg:min-h-[700px]"/>
                                            </div>
                                        </div>
                                    </TabsContent>
                                </div>
                            </div>
                        </div>
                    </Tabs>
                </div>
            </div>
        </>
    )
}
