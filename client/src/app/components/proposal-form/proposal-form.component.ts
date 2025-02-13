import { Component, inject } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { HttpClient, HttpClientModule } from "@angular/common/http";
import { HttpErrorResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { CommonModule } from "@angular/common";
import { MatIconModule } from "@angular/material/icon";
import { MarkdownModule } from "ngx-markdown";
import { MarkdownToHtmlModule } from "../../markdown-to-html.module";
import { HttpRequestsConstants } from "../../services/http-requests-constants";

interface ProposalData {
  customer: string;
  title: string;
  requirements: string;
}

interface ProposalSection {
  title: string;
  content: string;
  layout_rank: number;
}

interface GeneratedProposal {
  proposal: {
    [key: string]: ProposalSection;
  };
}

@Component({
  selector: "app-proposal-form",
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatIconModule,
    MarkdownModule,
    MarkdownToHtmlModule,
  ],
  templateUrl: "./proposal-form.component.html",
  styleUrls: ["./proposal-form.component.css"],
  providers: [HttpClient],
})
export class ProposalFormComponent {
  proposalForm: FormGroup;
  isLoading = false;
  proposal: ProposalSection[] = [];
  isEditing = false;

  private http = inject(HttpClient);
  private fb = inject(FormBuilder);

  constructor() {
    this.proposalForm = this.fb.group({
      customer: ["", Validators.required],
      title: ["", Validators.required],
      requirements: ["", Validators.required],
    });
  }

  generateProposal(data: ProposalData): Observable<GeneratedProposal> {
    return this.http.post<GeneratedProposal>(
      HttpRequestsConstants.GENERATE_PROPOSAL,
      data
    );
  }

  handleSubmit(): void {
    if (this.proposalForm.invalid) {
      return;
    }

    this.isLoading = true;

    this.generateProposal(this.proposalForm.value).subscribe(
      (result) => {
        const proposalSections = Object.values(result.proposal);
        proposalSections.sort((a, b) => a.layout_rank - b.layout_rank);
        this.proposal = proposalSections;
        this.isLoading = false;
      },
      (error: HttpErrorResponse) => {
        console.error("Error generating proposal:", error);
        this.isLoading = false;
      }
    );
  }

  toggleEdit(): void {
    this.isEditing = !this.isEditing;
  }

  downloadProposal(): void {
    const content = this.proposal
      .map(section => `# ${section.title}\n\n${section.content}`)
      .join('\n\n');
    
    const blob = new Blob([content], { 
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'proposal.docx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  get f() {
    return this.proposalForm.controls;
  }
}