import { Component, signal } from "@angular/core";
import { CommonModule } from "@angular/common";
import { ClientResearchComponent } from "./components/client-research/client-research.component";
import { ScriptGeneratorComponent } from "./components/script-generator/script-generator.component";
import { ChatInterfaceComponent } from "./components/chat-interface/chat-interface.component";
import { ProposalFormComponent } from "./components/proposal-form/proposal-form.component";
import { MatIconModule } from "@angular/material/icon";
import { ReactiveFormsModule } from "@angular/forms";
import { RouterOutlet } from "@angular/router";

type TabType = "research" | "chat" | "proposal";
type ResearchTabType = "client-research" | "script-generator";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    ClientResearchComponent,
    ScriptGeneratorComponent,
    ChatInterfaceComponent,
    ProposalFormComponent,
    ReactiveFormsModule,
    // RouterOutlet
  ],
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"],
})
export class AppComponent {
  activeTab = signal<TabType>("chat");

  researchTab = signal<ResearchTabType>("client-research");

  companyResearch = signal<string>("");

  getTabClass(tab: TabType): string {
    const baseClass =
      "flex items-center gap-2 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm";
    const activeClass = "border-blue-500 text-blue-600";
    const inactiveClass =
      "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300";

    return `${baseClass} ${
      this.activeTab() === tab ? activeClass : inactiveClass
    }`;
  }

  getResearchTabClass(tab: ResearchTabType): string {
    const baseClass =
      "flex items-center gap-2 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm";
    const activeClass = "border-blue-500 text-blue-600";
    const inactiveClass =
      "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300";

    return `${baseClass} ${
      this.researchTab() === tab ? activeClass : inactiveClass
    }`;
  }

  handleResearchComplete(researchData: string) {
    this.companyResearch.set(researchData);
  }
}
