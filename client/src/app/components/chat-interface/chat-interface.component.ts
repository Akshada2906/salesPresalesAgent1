import { Component, OnInit, SecurityContext } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { FormsModule } from "@angular/forms";
import { CommonModule } from "@angular/common";
import { ChatSidebarComponent } from "../chat-sidebar/chat-sidebar.component";
import { ChatMessageComponent } from "../chat-message/chat-message.component";
import { MatIconModule } from "@angular/material/icon";
import { DomSanitizer } from "@angular/platform-browser";

interface Message {
  text: string;
  isBot: boolean;
  timestamp: string;
  taskInfo?: {
    techStack?: {
      name: string;
      description: string;
      usage: string;
    }[];
  };
}

@Component({
  selector: "app-chat-interface",
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    ChatSidebarComponent,
    ChatMessageComponent,
    MatIconModule,
  ],
  templateUrl: "./chat-interface.component.html",
  styleUrls: ["./chat-interface.component.css"],
})
export class ChatInterfaceComponent implements OnInit {
  botMessage: any = [];
  messages: Message[] = [
    {
      text: "Hello! I'm your sales assistant. How can I help you today?",
      isBot: true,
      timestamp: new Date().toLocaleTimeString(),
      taskInfo: {
        techStack: [
          {
            name: "React",
            description: "A JavaScript library for building user interfaces",
            usage:
              "Used for building the frontend components and managing UI state",
          },
          {
            name: "TypeScript",
            description: "JavaScript with syntax for types",
            usage: "Ensures type safety and better developer experience",
          },
          {
            name: "Node.js",
            description: "JavaScript runtime built on Chrome's V8 engine",
            usage: "Powers the backend server and API endpoints",
          },
        ],
      },
    },
  ];
  input: string = "";
  isSidebarOpen: boolean = true;

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  ngOnInit(): void {}

  async callChatAPI(query: string) {
    try {
      const response = await this.http
        .post<any>("http://127.0.0.1:8000/chat_assistant", { query })
        .toPromise();
      return response;
    } catch (error) {
      console.error("Error calling chat API:", error);
      return {
        answer: "I'm sorry, I encountered an error processing your request.",
      };
    }
  }

  async handleSend() {
    if (!this.input.trim()) return;

    const newMessage: Message = {
      text: this.input,
      isBot: false,
      timestamp: new Date().toLocaleTimeString(),
    };

    this.messages.push(newMessage);
    this.input = "";

    const botAnswer = await this.callChatAPI(newMessage.text);

    const botResponse: Message = {
      text: botAnswer.message,
      isBot: true,
      timestamp: new Date().toLocaleTimeString(),
      taskInfo: {
        techStack: botAnswer.techs,
      },
    };

    if (botAnswer.companies_list) {
      const formattedList = this.formatCompaniesList(botAnswer.companies_list);
      botResponse.text += formattedList;
    }

    this.messages.push(botResponse);
  }

  formatCompaniesList(companiesList: any[]) {
    let formattedList =
      "<br><br>Here are some case studies of our previous clients:<br>";

    companiesList.forEach((company, index) => {
      formattedList += `
        <div class="company-case-study${index > 0 ? " mt-4" : ""}">
          <p><strong>Client:</strong> ${
            this.sanitizer.sanitize(SecurityContext.HTML, company["Client"]) ||
            ""
          }</p>
          <p><strong>Business Challenge:</strong> ${
            this.sanitizer.sanitize(
              SecurityContext.HTML,
              company["Business Challenge"]
            ) || ""
          }</p>
          <p><strong>Our Solution:</strong> ${
            this.sanitizer.sanitize(
              SecurityContext.HTML,
              company["Our Solution"]
            ) || ""
          }</p>
          <p><strong>Technologies Used:</strong> ${
            this.sanitizer.sanitize(
              SecurityContext.HTML,
              company["Technologies Used"]
            ) || ""
          }</p>
        </div>
      `;
    });

    return formattedList;
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  get currentTaskInfo() {
    return this.messages[this.messages.length - 1]?.taskInfo;
  }
}
